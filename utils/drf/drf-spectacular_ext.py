import textwrap
from typing import Optional

from django.utils.encoding import force_str
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import ComponentRegistry
from drf_spectacular.utils import _SchemaType


def force_real_str(s, encoding="utf-8", strings_only=False, errors="strict"):
    """
    Force `s` into a ``str`` instance.
    """
    if s is not None:
        s = force_str(s, encoding, strings_only, errors)
        s = str(s)

        # Remove common indentation to get the correct Markdown rendering
        s = textwrap.dedent(s)

    return s


TO_HANDLE_DOC_STRING_FIELDS = [
    "summary",
    "description",
]


class AutoSchemaWithDocString(AutoSchema):
    def get_operation(
        self,
        path: str,
        path_regex: str,
        path_prefix: str,
        method: str,
        registry: ComponentRegistry,
    ) -> Optional[_SchemaType]:
        operation = super().get_operation(
            path,
            path_regex,
            path_prefix,
            method,
            registry,
        )

        if operation is not None:
            for field in TO_HANDLE_DOC_STRING_FIELDS:
                if field in operation:
                    operation[field] = force_real_str(operation[field])

            if "parameters" in operation:
                parameters = operation["parameters"]
                for p in parameters:
                    for field in TO_HANDLE_DOC_STRING_FIELDS:
                        if field in p:
                            p[field] = force_real_str(p[field])

        return operation
