"""
String to type annotation map that find type annotation by method and argument name.
"""

from collections.abc import Mapping
from typing import TypeVar

from boto3.dynamodb.table import BatchWriter

from mypy_boto3_builder.constants import ALL, CLIENT
from mypy_boto3_builder.service_name import ServiceName, ServiceNameCatalog
from mypy_boto3_builder.type_annotations.external_import import ExternalImport
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type import Type
from mypy_boto3_builder.type_annotations.type_constant import TypeConstant
from mypy_boto3_builder.type_annotations.type_subscript import TypeSubscript
from mypy_boto3_builder.type_maps.literals import QueueAttributeFilterType
from mypy_boto3_builder.type_maps.named_unions import (
    ConditionBaseImportTypeDef,
    CopySourceOrStrTypeDef,
)
from mypy_boto3_builder.type_maps.typed_dicts import CopySourceTypeDef

__all__ = ("get_method_type_stub",)

_T = TypeVar("_T", bound=FakeAnnotation)
ServiceTypeMap = Mapping[ServiceName, Mapping[str, Mapping[str, Mapping[str, _T]]]]


DEFAULT_VALUE_MAP: ServiceTypeMap[TypeConstant] = {
    ServiceNameCatalog.glacier: {
        CLIENT: {
            ALL: {
                "accountId": TypeConstant("-"),
            }
        }
    },
}

TYPE_MAP: ServiceTypeMap[FakeAnnotation] = {
    ServiceNameCatalog.s3: {
        # FIXME: boto3 overrides CopySource parameters for some S3 methods.
        # Types are set according to docs, might be incorrect
        CLIENT: {
            "copy_object": {"CopySource": CopySourceOrStrTypeDef},
            "upload_part_copy": {"CopySource": CopySourceOrStrTypeDef},
            "copy": {"CopySource": CopySourceTypeDef},
        },
        "MultipartUploadPart": {
            "copy_from": {"CopySource": CopySourceOrStrTypeDef},
        },
        "Bucket": {"copy": {"CopySource": CopySourceTypeDef}},
        "Object": {
            "copy": {"CopySource": CopySourceTypeDef},
            "copy_from": {"CopySource": CopySourceOrStrTypeDef},
        },
        "ObjectSummary": {"copy_from": {"CopySource": CopySourceOrStrTypeDef}},
        # FIXME: https://github.com/boto/boto3/issues/3501
        "MultipartUpload": {"Part": {"part_number": Type.int}},
    },
    ServiceNameCatalog.dynamodb: {
        "Table": {
            "batch_writer": {"return": ExternalImport.from_class(BatchWriter)},
            "query": {
                "KeyConditionExpression": ConditionBaseImportTypeDef,
                "FilterExpression": ConditionBaseImportTypeDef,
                "ConditionExpression": ConditionBaseImportTypeDef,
            },
            "delete_item": {
                "ConditionExpression": ConditionBaseImportTypeDef,
            },
            "put_item": {
                "ConditionExpression": ConditionBaseImportTypeDef,
            },
            "update_item": {
                "ConditionExpression": ConditionBaseImportTypeDef,
            },
            "scan": {
                "FilterExpression": ConditionBaseImportTypeDef,
            },
        },
    },
    ServiceNameCatalog.sqs: {
        ALL: {
            # FIXME: https://github.com/boto/botocore/issues/2726
            "receive_messages": {
                "AttributeNames": TypeSubscript(Type.Sequence, [QueueAttributeFilterType]),
            },
            "receive_message": {
                "AttributeNames": TypeSubscript(Type.Sequence, [QueueAttributeFilterType]),
            },
            "get_queue_attributes": {
                "AttributeNames": TypeSubscript(Type.Sequence, [QueueAttributeFilterType]),
            },
        }
    },
}


def _get_from_service_map(
    service_name: ServiceName,
    class_name: str,
    method_name: str,
    argument_name: str,
    service_type_map: ServiceTypeMap[_T],
) -> _T | None:
    if service_name not in service_type_map:
        return None

    checks = (
        (class_name, method_name, argument_name),
        (class_name, ALL, argument_name),
        (ALL, method_name, argument_name),
        (ALL, ALL, argument_name),
    )
    class_type_map = service_type_map[service_name]

    for check_class_name, check_method_name, check_argument_name in checks:
        if check_class_name not in class_type_map:
            continue

        method_type_map = class_type_map[check_class_name]

        if check_method_name not in method_type_map:
            continue

        operation_type_map = method_type_map[check_method_name]
        if check_argument_name in operation_type_map:
            return operation_type_map[check_argument_name]

    return None


def get_method_type_stub(
    service_name: ServiceName, class_name: str, method_name: str, argument_name: str
) -> FakeAnnotation | None:
    """
    Get stub type for method argument.

    Arguments:
        service_name -- Service name.
        class_name -- Parent class name.
        method_name -- Method name.
        argument_name -- Argument name.

    Returns:
        Type annotation or None.
    """
    return _get_from_service_map(service_name, class_name, method_name, argument_name, TYPE_MAP)


def get_default_value_stub(
    service_name: ServiceName, class_name: str, method_name: str, argument_name: str
) -> TypeConstant | None:
    """
    Get default value stub for method argument.

    Arguments:
        service_name -- Service name.
        class_name -- Parent class name.
        method_name -- Method name.
        argument_name -- Argument name.

    Returns:
        TypeConstant or None.
    """
    return _get_from_service_map(
        service_name, class_name, method_name, argument_name, DEFAULT_VALUE_MAP
    )
