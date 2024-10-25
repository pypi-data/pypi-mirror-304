import asyncio
import types
import functools
from collections import defaultdict
from dataclasses import is_dataclass
from inspect import iscoroutine, isfunction
from typing import Any, DefaultDict, Sequence, Type, TypeVar, List, Callable, Optional, Mapping, Union, Iterator, Dict, get_type_hints
import pydantic_resolve.constant as const
from pydantic_resolve.exceptions import GlobalLoaderFieldOverlappedError
from aiodataloader import DataLoader
from pydantic_resolve.compat import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic import BaseModel, TypeAdapter, ValidationError
else:
    from pydantic import BaseModel, parse_obj_as, ValidationError

def get_class_field_annotations(cls: Type):
    anno = cls.__dict__.get('__annotations__') or {}
    return anno.keys()


T = TypeVar("T")
V = TypeVar("V")

if PYDANTIC_V2:
    class TypeAdapterManager:
        apapters = {}
        
        @classmethod
        def get(cls, type):
            adapter = cls.apapters.get(type)
            if adapter:
                return adapter
            else:
                new_adapter = TypeAdapter(type)
                cls.apapters[type] = new_adapter
                return new_adapter

def safe_issubclass(kls, classinfo):
    try:
        return issubclass(kls, classinfo)
    except TypeError:
        return False

def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]):
    overlap = set(a.keys()) & set(b.keys())
    if overlap:
        raise GlobalLoaderFieldOverlappedError(f'loader_params and global_loader_param have duplicated key(s): {",".join(overlap)}')
    else:
        return {**a, **b}

def build_object(items: Sequence[T], keys: List[V], get_pk: Callable[[T], V]) -> Iterator[Optional[T]]:
    """
    helper function to build return object data required by aiodataloader
    """
    dct: Mapping[V, T] = {}
    for item in items:
        _key = get_pk(item)
        dct[_key] = item
    results = (dct.get(k, None) for k in keys)
    return results

def build_list(items: Sequence[T], keys: List[V], get_pk: Callable[[T], V]) -> Iterator[List[T]]:
    """
    helper function to build return list data required by aiodataloader
    """
    dct: DefaultDict[V, List[T]] = defaultdict(list) 
    for item in items:
        _key = get_pk(item)
        dct[_key].append(item)
    results = (dct.get(k, []) for k in keys)
    return results

def replace_method(cls: Type, cls_name: str, func_name: str, func: Callable):
    """test-only"""
    KLS = type(cls_name, (cls,), {func_name: func})
    return KLS

def get_required_fields(kls: BaseModel):
    required_fields = []

    def _is_require(field):
        if PYDANTIC_V2:
            return field.is_required()
        else:
            return field.required

    # 1. get required fields
    if PYDANTIC_V2:
        items = kls.model_fields.items()
    else:
        items = kls.__fields__.items()
    

    for fname, field in items:
        if _is_require(field):
            required_fields.append(fname)
        

    # 2. get resolve_ and post_ target fields
    for f in dir(kls):
        if f.startswith(const.RESOLVE_PREFIX):
            if isfunction(getattr(kls, f)):
                required_fields.append(f.replace(const.RESOLVE_PREFIX, ''))

        if f.startswith(const.POST_PREFIX):
            if isfunction(getattr(kls, f)):
                required_fields.append(f.replace(const.POST_PREFIX, ''))

    return required_fields


def output_v1(kls):
    """
    set required as True for all fields, make typescript code gen result friendly to use
    """
    if safe_issubclass(kls, BaseModel):
        def _schema_extra(schema: Dict[str, Any], model) -> None:
            fnames = get_required_fields(model)
            schema['required'] = fnames

        kls.__config__.schema_extra = staticmethod(_schema_extra)

    else:
        raise AttributeError(f'target class {kls.__name__} is not BaseModel')
    return kls

def output_v2(kls):
    """
    set required as True for all fields
    make typescript code gen result friendly to use
    """

    if safe_issubclass(kls, BaseModel):

        def build():
            def schema_extra(schema: Dict[str, Any], model) -> None:
                fnames = get_required_fields(model)
                schema['required'] = fnames
            return schema_extra

        kls.model_config['json_schema_extra'] = staticmethod(build())

    else:
        raise AttributeError(f'target class {kls.__name__} is not BaseModel')
    return kls

output = output_v2 if PYDANTIC_V2 else output_v1


def model_config_v1(default_required: bool = True):
    """
    - hidden_fields: fields want to hide
    - default_required: 
        if resolve field has default value, it will not be listed in schema['required']
        set default_required=True to add it into required list.
    """
    def wrapper(kls):
        if safe_issubclass(kls, BaseModel):
                
            # override schema_extra method
            def _schema_extra(schema: Dict[str, Any], model) -> None:
                # define schema.properties
                excludes = set()

                if kls.__exclude_fields__:
                    for k in kls.__exclude_fields__.keys():
                        excludes.add(k)

                props = {}
                for k, v in schema.get('properties', {}).items():
                    if k not in excludes:
                        props[k] = v
                schema['properties'] = props

                # define schema.required
                if default_required:
                    fnames = get_required_fields(model)
                    schema['required'] = fnames
            kls.__config__.schema_extra = staticmethod(_schema_extra)
        else:
            raise AttributeError(f'target class {kls.__name__} is not BaseModel')
        return kls
    return wrapper

def model_config_v2(default_required: bool=True):
    """
    in pydantic v2, we can not use __exclude_field__ to set hidden field in model_config hidden_field params
    model_config now is just a simple decorator to remove fields (with exclude=True) from schema.properties
    and set schema.required for better schema description. 
    (same like `output` decorator, you can replace output with model_config)

    it keeps the form of model_config(params) in order to extend new features in future
    """
    def wrapper(kls):
        if safe_issubclass(kls, BaseModel):
            def build():
                def _schema_extra(schema: Dict[str, Any], model) -> None:
                    # 1. collect exclude fields and then hide in both schema and dump (default action)
                    excluded_fields = [k for k, v in kls.model_fields.items() if v.exclude == True]
                    props = {}

                    # config schema properties
                    for k, v in schema.get('properties', {}).items():
                        if k not in excluded_fields:
                            props[k] = v
                    schema['properties'] = props

                    # config schema required (fields with default values will not be listed in required field)
                    # and the generated typescript models will define it as optional, and is troublesome in use
                    if default_required:
                        fnames = get_required_fields(model)
                        if excluded_fields:
                            fnames = [n for n in fnames if n not in excluded_fields]
                        schema['required'] = fnames

                return _schema_extra

            kls.model_config['json_schema_extra'] = staticmethod(build())
        else:
            raise AttributeError(f'target class {kls.__name__} is not BaseModel')
        return kls
    return wrapper

model_config = model_config_v2 if PYDANTIC_V2 else model_config_v1


def mapper(func_or_class: Union[Callable, Type]):
    """
    execute post-transform function after the value is reolved
    func_or_class:
        is func: run func
        is class: call auto_mapping to have a try
    """
    def inner(inner_fn):

        # if mapper provided, auto map from target type will be disabled
        setattr(inner_fn, const.HAS_MAPPER_FUNCTION, True)

        @functools.wraps(inner_fn)
        async def wrap(*args, **kwargs):

            retVal = inner_fn(*args, **kwargs)
            while iscoroutine(retVal) or asyncio.isfuture(retVal):
                retVal = await retVal  # get final result
            
            if retVal is None:
                return None

            if isinstance(func_or_class, types.FunctionType):
                # manual mapping
                return func_or_class(retVal)
            else:
                # auto mapping
                if isinstance(retVal, list):
                    if retVal:
                        rule = _get_mapping_rule(func_or_class, retVal[0])
                        return _apply_rule(rule, func_or_class, retVal, True)
                    else:
                        return retVal  # return []
                else:
                    rule = _get_mapping_rule(func_or_class, retVal)
                    return _apply_rule(rule, func_or_class, retVal, False)
        return wrap
    return inner

def _get_mapping_rule_v1(target, source) -> Optional[Callable]:
    # do noting
    if isinstance(source, target):
        return None

    # pydantic
    if safe_issubclass(target, BaseModel):
        if target.__config__.orm_mode:
            if isinstance(source, dict):
                raise AttributeError(f"{type(source)} -> {target.__name__}: pydantic from_orm can't handle dict object")
            else:
                return lambda t, s: t.from_orm(s)

        if isinstance(source, (dict, BaseModel)):
            return lambda t, s: t.parse_obj(s)

        else:
            raise AttributeError(f"{type(source)} -> {target.__name__}: pydantic can't handle non-dict data")

    # dataclass
    if is_dataclass(target):
        if isinstance(source, dict):
            return lambda t, s: t(**s)

    raise NotImplementedError(f"{type(source)} -> {target.__name__}: faild to get auto mapping rule and execut mapping, use your own rule instead.")

def _get_mapping_rule_v2(target, source) -> Optional[Callable]:
    # do noting
    if isinstance(source, target):
        return None

    # pydantic
    if safe_issubclass(target, BaseModel):
        if target.model_config.get('from_attributes'):
            if isinstance(source, dict):
                raise AttributeError(f"{type(source)} -> {target.__name__}: pydantic from_orm can't handle dict object")
            else:
                return lambda t, s: t.model_validate(s)

        if isinstance(source, dict):
            return lambda t, s: t.model_validate(s)

        if isinstance(source, BaseModel):
            if source.model_config.get('from_attributes'):
                return lambda t, s: t.model_validate(s) 
            else:
                return lambda t, s: t(**s.model_dump()) 

        else:
            raise AttributeError(f"{type(source)} -> {target.__name__}: pydantic can't handle non-dict data")
    
    # dataclass
    if is_dataclass(target):
        if isinstance(source, dict):
            return lambda t, s: t(**s)
    
    raise NotImplementedError(f"{type(source)} -> {target.__name__}: faild to get auto mapping rule and execut mapping, use your own rule instead.")

_get_mapping_rule = _get_mapping_rule_v2 if PYDANTIC_V2 else _get_mapping_rule_v1


def _apply_rule(rule: Optional[Callable], target, source: Any, is_list: bool):
    if not rule:  # no change
        return source

    if is_list:
        return [rule(target, s) for s in source]
    else:
        return rule(target, source)

def ensure_subset_v1(base):
    """
    used with pydantic class to make sure a class's field is 
    subset of target class
    """
    def wrap(kls):
        assert safe_issubclass(base, BaseModel), 'base should be pydantic class'
        assert safe_issubclass(kls, BaseModel), 'class should be pydantic class'

        @functools.wraps(kls)
        def inner():
            for k, field in kls.__fields__.items():
                if field.required:
                    base_field = base.__fields__.get(k)
                    if not base_field:
                        raise AttributeError(f'{k} not existed in {base.__name__}.')
                    if base_field and base_field.type_ != field.type_:
                        raise AttributeError(f'type of {k} not consistent with {base.__name__}'  )
            return kls
        return inner()
    return wrap 

def ensure_subset_v2(base):
    """
    used with pydantic class to make sure a class's field is 
    subset of target class
    """
    def wrap(kls):
        assert safe_issubclass(base, BaseModel), 'base should be pydantic class'
        assert safe_issubclass(kls, BaseModel), 'class should be pydantic class'

        @functools.wraps(kls)
        def inner():
            for k, field in kls.model_fields.items():
                if field.is_required():
                    base_field = base.model_fields.get(k)
                    if not base_field:
                        raise AttributeError(f'{k} not existed in {base.__name__}.')
                    if base_field and base_field.annotation != field.annotation:
                        raise AttributeError(f'type of {k} not consistent with {base.__name__}'  )
            return  kls
        return inner()
    return wrap

ensure_subset = ensure_subset_v2 if PYDANTIC_V2 else ensure_subset_v1


def update_forward_refs(kls):
    def update_pydantic_forward_refs(kls: Type[BaseModel]):
        """
        recursively update refs.
        """
        if getattr(kls, const.PYDANTIC_FORWARD_REF_UPDATED, False):
            return

        if PYDANTIC_V2:
            kls.model_rebuild()
        else:
            kls.update_forward_refs()

        setattr(kls, const.PYDANTIC_FORWARD_REF_UPDATED, True)

        if PYDANTIC_V2:
            values = kls.model_fields.values()
        else:
            values = kls.__fields__.values()

        for field in values:
            if PYDANTIC_V2:
                shelled_type = shelling_type(field.annotation)
            else:
                shelled_type = shelling_type(field.type_)
            update_forward_refs(shelled_type)

    def update_dataclass_forward_refs(kls):
        if not getattr(kls, const.DATACLASS_FORWARD_REF_UPDATED, False):
            anno = get_type_hints(kls)
            kls.__annotations__ = anno
            setattr(kls, const.DATACLASS_FORWARD_REF_UPDATED, True)

            for _, v in kls.__annotations__.items():
                shelled_type = shelling_type(v)
                update_forward_refs(shelled_type)

    if safe_issubclass(kls, BaseModel):
        update_pydantic_forward_refs(kls)

    if is_dataclass(kls):
        update_dataclass_forward_refs(kls)


def try_parse_data_to_target_field_type_v1(target, field_name, data):
    """
    parse to pydantic or dataclass object
    1. get type of target field
    2. parse
    """
    field_type = None

    # 1. get type of target field
    if isinstance(target, BaseModel):
        _fields = target.__class__.__fields__
        field_type = _fields[field_name].outer_type_

        # handle optional logic
        if data is None and _fields[field_name].required == False:
            return data

    elif is_dataclass(target):
        field_type = target.__class__.__annotations__[field_name]

    # 2. parse
    if field_type:
        try:
            result = parse_obj_as(field_type, data)
            return result
        except ValidationError as e:
            print(f'Warning: type mismatch, pls check the return type for "{field_name}", expected: {field_type}')
            raise e
    else:
        return data  #noqa

def try_parse_data_to_target_field_type_v2(target, field_name, data):
    """
    parse to pydantic or dataclass object
    1. get type of target field
    2. parse
    """
    field_type = None

    # 1. get type of target field
    if isinstance(target, BaseModel):
        _fields = target.__class__.model_fields
        field_type = _fields[field_name].annotation

        # handle optional logic
        if data is None and _fields[field_name].is_required() == False:
            return data

    elif is_dataclass(target):
        field_type = target.__class__.__annotations__[field_name]

    # 2. parse
    if field_type:
        try:
            # https://docs.pydantic.dev/latest/concepts/performance/#typeadapter-instantiated-once
            adapter = TypeAdapterManager.get(field_type)
            result = adapter.validate_python(data)  
            return result
        except ValidationError as e:
            print(f'Warning: type mismatch, pls check the return type for "{field_name}", expected: {field_type}')
            raise e
    
    else:
        return data  #noqa

try_parse_data_to_target_field_type = try_parse_data_to_target_field_type_v2 if PYDANTIC_V2 else try_parse_data_to_target_field_type_v1

def _is_optional(annotation):
    annotation_origin = getattr(annotation, "__origin__", None)
    return annotation_origin == Union \
        and len(annotation.__args__) == 2 \
        and annotation.__args__[1] == type(None)  # noqa

def _is_list(annotation):
    return getattr(annotation, "__origin__", None) == list

def shelling_type(type):
    while _is_optional(type) or _is_list(type):
        type = type.__args__[0]
    return type

def get_kls_full_path(kls):
    return f'{kls.__module__}.{kls.__qualname__}'

def copy_dataloader_kls(name, loader_kls):
    """
    quickly copy from an existed DataLoader class
    usage:
    SeniorMemberLoader = copy_dataloader('SeniorMemberLoader', ul.UserByLevelLoader)
    JuniorMemberLoader = copy_dataloader('JuniorMemberLoader', ul.UserByLevelLoader)
    """
    return type(name, loader_kls.__bases__, dict(loader_kls.__dict__))

class StrictEmptyLoader(DataLoader):
    async def batch_load_fn(self, keys):
        """it should not be triggered, otherwise will raise Exception"""
        raise ValueError('EmptyLoader should load from pre loaded data')

class ListEmptyLoader(DataLoader):
    async def batch_load_fn(self, keys):
        dct = {}
        return [dct.get(k, []) for k in keys]

class SingleEmptyLoader(DataLoader):
    async def batch_load_fn(self, keys):
        dct = {}
        return [dct.get(k, None) for k in keys]

def generate_strict_empty_loader(name):
    """generated Loader will raise ValueError if not found"""
    return type(name, StrictEmptyLoader.__bases__, dict(StrictEmptyLoader.__dict__))  #noqa

def generate_list_empty_loader(name):
    """generated Loader will return [] if not found"""
    return type(name, ListEmptyLoader.__bases__, dict(ListEmptyLoader.__dict__))  #noqa

def generate_single_empty_loader(name):
    """generated Loader will return None if not found"""
    return type(name, SingleEmptyLoader.__bases__, dict(SingleEmptyLoader.__dict__))  #noqa