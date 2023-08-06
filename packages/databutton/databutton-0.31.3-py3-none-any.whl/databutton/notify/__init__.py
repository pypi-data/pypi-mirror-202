from .email import (
    attachment_from_bytes,
    attachment_from_dataframe_as_csv,
    attachment_from_dataframe_as_excel,
    attachment_from_file,
    attachment_from_pil_image_as_jpeg,
    attachment_from_str,
    email,
)

__all__ = [
    "email",
    "attachment_from_bytes",
    "attachment_from_str",
    "attachment_from_file",
    "attachment_from_pil_image_as_jpeg",
    "attachment_from_dataframe_as_csv",
    "attachment_from_dataframe_as_excel",
]
