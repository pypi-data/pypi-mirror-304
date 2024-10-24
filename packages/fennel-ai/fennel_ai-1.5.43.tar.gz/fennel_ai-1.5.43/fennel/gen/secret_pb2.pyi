"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class SecretRef(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ARN_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    secret_arn: builtins.str
    role_arn: builtins.str
    @property
    def path(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Next id: 4"""
    def __init__(
        self,
        *,
        secret_arn: builtins.str = ...,
        role_arn: builtins.str | None = ...,
        path: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_role_arn", b"_role_arn", "role_arn", b"role_arn"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_role_arn", b"_role_arn", "path", b"path", "role_arn", b"role_arn", "secret_arn", b"secret_arn"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_role_arn", b"_role_arn"]) -> typing_extensions.Literal["role_arn"] | None: ...

global___SecretRef = SecretRef
