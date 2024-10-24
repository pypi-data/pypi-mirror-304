"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import expression_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import metadata_pb2
import pycode_pb2
import schema_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ExtractorType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ExtractorTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ExtractorType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PY_FUNC: _ExtractorType.ValueType  # 0
    """user supplied python extractor function"""
    LOOKUP: _ExtractorType.ValueType  # 1
    ALIAS: _ExtractorType.ValueType  # 2
    EXPR: _ExtractorType.ValueType  # 3

class ExtractorType(_ExtractorType, metaclass=_ExtractorTypeEnumTypeWrapper): ...

PY_FUNC: ExtractorType.ValueType  # 0
"""user supplied python extractor function"""
LOOKUP: ExtractorType.ValueType  # 1
ALIAS: ExtractorType.ValueType  # 2
EXPR: ExtractorType.ValueType  # 3
global___ExtractorType = ExtractorType

@typing_extensions.final
class CoreFeatureset(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    PYCODE_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def metadata(self) -> metadata_pb2.Metadata: ...
    @property
    def pycode(self) -> pycode_pb2.PyCode: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        metadata: metadata_pb2.Metadata | None = ...,
        pycode: pycode_pb2.PyCode | None = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "pycode", b"pycode"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "name", b"name", "pycode", b"pycode", "tags", b"tags"]) -> None: ...

global___CoreFeatureset = CoreFeatureset

@typing_extensions.final
class Feature(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DTYPE_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    FEATURE_SET_NAME_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def dtype(self) -> schema_pb2.DataType: ...
    @property
    def metadata(self) -> metadata_pb2.Metadata: ...
    feature_set_name: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        dtype: schema_pb2.DataType | None = ...,
        metadata: metadata_pb2.Metadata | None = ...,
        feature_set_name: builtins.str = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "feature_set_name", b"feature_set_name", "metadata", b"metadata", "name", b"name", "tags", b"tags"]) -> None: ...

global___Feature = Feature

@typing_extensions.final
class FieldLookupInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FIELD_FIELD_NUMBER: builtins.int
    DEFAULT_VALUE_FIELD_NUMBER: builtins.int
    @property
    def field(self) -> schema_pb2.Field: ...
    default_value: builtins.str
    """expected to be sent as json"""
    def __init__(
        self,
        *,
        field: schema_pb2.Field | None = ...,
        default_value: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["field", b"field"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["default_value", b"default_value", "field", b"field"]) -> None: ...

global___FieldLookupInfo = FieldLookupInfo

@typing_extensions.final
class Extractor(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DATASETS_FIELD_NUMBER: builtins.int
    INPUTS_FIELD_NUMBER: builtins.int
    FEATURES_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    PYCODE_FIELD_NUMBER: builtins.int
    FEATURE_SET_NAME_FIELD_NUMBER: builtins.int
    EXTRACTOR_TYPE_FIELD_NUMBER: builtins.int
    FIELD_INFO_FIELD_NUMBER: builtins.int
    EXPR_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def datasets(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def inputs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Input]: ...
    @property
    def features(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The features that this extractor produces"""
    @property
    def metadata(self) -> metadata_pb2.Metadata: ...
    version: builtins.int
    @property
    def pycode(self) -> pycode_pb2.PyCode:
        """required iff extractor_type == PY_FUNC"""
    feature_set_name: builtins.str
    extractor_type: global___ExtractorType.ValueType
    @property
    def field_info(self) -> global___FieldLookupInfo:
        """pycode excluded from the oneof for better bwd compatibility in Rust
        required iff extractor_type == LOOKUP
        """
    @property
    def expr(self) -> expression_pb2.Expr:
        """required iff extractor_type == EXPR"""
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        datasets: collections.abc.Iterable[builtins.str] | None = ...,
        inputs: collections.abc.Iterable[global___Input] | None = ...,
        features: collections.abc.Iterable[builtins.str] | None = ...,
        metadata: metadata_pb2.Metadata | None = ...,
        version: builtins.int = ...,
        pycode: pycode_pb2.PyCode | None = ...,
        feature_set_name: builtins.str = ...,
        extractor_type: global___ExtractorType.ValueType = ...,
        field_info: global___FieldLookupInfo | None = ...,
        expr: expression_pb2.Expr | None = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["derived_extractor_info", b"derived_extractor_info", "expr", b"expr", "field_info", b"field_info", "metadata", b"metadata", "pycode", b"pycode"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["datasets", b"datasets", "derived_extractor_info", b"derived_extractor_info", "expr", b"expr", "extractor_type", b"extractor_type", "feature_set_name", b"feature_set_name", "features", b"features", "field_info", b"field_info", "inputs", b"inputs", "metadata", b"metadata", "name", b"name", "pycode", b"pycode", "tags", b"tags", "version", b"version"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["derived_extractor_info", b"derived_extractor_info"]) -> typing_extensions.Literal["field_info"] | None: ...

global___Extractor = Extractor

@typing_extensions.final
class Input(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class Feature(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        FEATURE_SET_NAME_FIELD_NUMBER: builtins.int
        NAME_FIELD_NUMBER: builtins.int
        feature_set_name: builtins.str
        name: builtins.str
        def __init__(
            self,
            *,
            feature_set_name: builtins.str = ...,
            name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["feature_set_name", b"feature_set_name", "name", b"name"]) -> None: ...

    FEATURE_FIELD_NUMBER: builtins.int
    DTYPE_FIELD_NUMBER: builtins.int
    @property
    def feature(self) -> global___Input.Feature: ...
    @property
    def dtype(self) -> schema_pb2.DataType: ...
    def __init__(
        self,
        *,
        feature: global___Input.Feature | None = ...,
        dtype: schema_pb2.DataType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "feature", b"feature"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dtype", b"dtype", "feature", b"feature"]) -> None: ...

global___Input = Input

@typing_extensions.final
class Model(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    INPUTS_FIELD_NUMBER: builtins.int
    OUTPUTS_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def inputs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Feature]: ...
    @property
    def outputs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Feature]: ...
    @property
    def metadata(self) -> metadata_pb2.Metadata: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        inputs: collections.abc.Iterable[global___Feature] | None = ...,
        outputs: collections.abc.Iterable[global___Feature] | None = ...,
        metadata: metadata_pb2.Metadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["inputs", b"inputs", "metadata", b"metadata", "name", b"name", "outputs", b"outputs"]) -> None: ...

global___Model = Model
