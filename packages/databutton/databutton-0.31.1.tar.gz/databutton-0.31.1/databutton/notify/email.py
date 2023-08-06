import base64
import io
import mimetypes
import re
from collections.abc import Sequence
from typing import List, Optional, Union

import pandas as pd
from pydantic import BaseModel

from .send import send


def valid_email(recipient: str) -> bool:
    # Note: We could possibly use some email validation library but it's tricky
    parts = recipient.split("@")
    if len(parts) != 2:
        return False
    return bool(parts[0] and parts[1])


def validate_email_to_arg(to: Union[str, List[str]]) -> List[str]:
    if isinstance(to, str):
        to = [to]
    if not isinstance(to, (list, tuple)) and len(to) > 0:
        raise ValueError(
            "Invalid recipient, expecting 'to' to be a string or list of strings."
        )
    invalid_emails = []
    for recipient in to:
        if not valid_email(recipient):
            invalid_emails.append(recipient)
    if invalid_emails:
        raise ValueError("\n".join(["Invalid email address(es):"] + invalid_emails))
    return to


# This is the type expected in the api
class Attachment(BaseModel):
    """An attachment to be included with an email."""

    # Attachment file name
    file_name: Optional[str] = None

    # MIME type of the attachment
    content_type: Optional[str] = None

    # Content ID (CID) to use for inline attachments
    content_id: Optional[str] = None

    # Base64 encoded data
    content_base64: str


# This is the type expected in the api
class Email(BaseModel):
    to: Union[str, List[str]]
    subject: str
    content_text: Optional[str] = None
    content_html: Optional[str] = None
    attachments: list[Attachment] = []


def determine_type(type: Optional[str], name: Optional[str]) -> Optional[str]:
    if type:
        return type
    if name:
        type, encoding = mimetypes.guess_type(name)
        # if encoding is not None:
        #     return "; ".join([type, encoding])
        return type
    return None


def encode_content(content: bytes | str) -> str:
    if isinstance(content, str):
        content = content.encode()
    return base64.b64encode(content).decode()


def attachment_from_bytes(
    content: bytes,
    *,
    file_name: Optional[str] = None,
    content_type: Optional[str] = None,
    cid: Optional[str] = None,
) -> Attachment:
    """Create attachment with content as raw bytes.

    You can optionally provide a file name and/or content type.

    If missing we will try to guess the content type from the file name.

    To use an attachment as an inline image in the email,
    set the `cid="my_image_id"` parameter,
    and use `<img src="cid:my_image_id">` in the html content.
    """
    return Attachment(
        file_name=file_name,
        content_type=determine_type(content_type, file_name),
        content_base64=encode_content(content),
        content_id=cid,
    )


def attachment_from_str(
    content: str,
    *,
    file_name: Optional[str] = None,
    content_type: Optional[str] = None,
    cid: Optional[str] = None,
) -> Attachment:
    """Create attachment with content as raw str."""
    return attachment_from_bytes(
        content.encode(),
        file_name=file_name,
        content_type=content_type,
        cid=cid,
    )


def attachment_from_file(
    fp: Optional[io.IOBase] = None,
    *,
    file_name: Optional[str] = None,
    content_type: Optional[str] = None,
    cid: Optional[str] = None,
) -> Attachment:
    """Create attachment with content from a file.

    fp can be anything with a .read() method returning bytes or str,
    or omitted to read file_name from file system.
    """
    if fp is None:
        if file_name is None:
            raise ValueError("Either `fp` or `file_name` must be provided.")
        with open(file_name, "rb") as fp:
            buf = fp.read()
    else:
        buf = fp.read()
        if isinstance(buf, str):
            buf = buf.encode()
    return attachment_from_bytes(
        buf,
        file_name=file_name,
        content_type=content_type,
        cid=cid,
    )


def attachment_from_pil_image_as_jpeg(
    image,  # PIL image
    *,
    image_format: str = "JPEG",
    file_name: Optional[str] = None,
    content_type: Optional[str] = None,
    cid: Optional[str] = None,
) -> Attachment:
    """Create image attachment with content from a PIL compatible image (such as pillow).

    This convenience function calls image.save(buffer, format=image_format),
    to further customize image formats etc take a peek at the implementation
    here and use attachment_from_bytes directly instead.

    You can optionally provide a file name and/or content type.

    If missing we will try to guess the content type from the file name.

    To use an attachment as an inline image in the email,
    set the `cid="my_image_id"` parameter,
    and use `<img src="cid:my_image_id">` in the html content.
    """
    buf = io.BytesIO()
    image.save(buf, format=image_format)
    return attachment_from_bytes(
        buf.getvalue(),
        file_name=file_name,
        content_type=content_type,
        cid=cid,
    )


def attachment_from_dataframe_as_csv(
    df: pd.DataFrame,
    *,
    file_name: Optional[str] = None,
) -> Attachment:
    """Create CSV attachment with content from a pandas dataframe."""
    return attachment_from_str(
        df.to_csv(),
        file_name=file_name,
        content_type="text/csv",
    )


MIME_TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def attachment_from_dataframe_as_excel(
    df: pd.DataFrame,
    *,
    file_name: Optional[str] = None,
) -> Attachment:
    """Create Excel (.xlsx) attachment with content from a pandas dataframe.

    Requires the openpyxl package to be installed.
    """
    buf = io.BytesIO()
    df.to_excel(buf)
    return attachment_from_bytes(
        buf.getvalue(),
        file_name=file_name,
        content_type=MIME_TYPE_XLSX,
    )


def validate_attachment(att: Attachment) -> Attachment:
    assert isinstance(att, Attachment)
    assert att.content_type
    assert att.file_name
    assert att.content_base64
    assert isinstance(att.content_base64, str)
    assert re.match(r"^[A-Za-z0-9+/=]+$", att.content_base64)
    return att


def create_email(
    *,
    to: Union[str, List[str]],
    subject: str,
    content_text: Optional[str] = None,
    content_html: Optional[str] = None,
    attachments: Sequence[Attachment] = (),
) -> Email:
    attachments = [validate_attachment(att) for att in attachments]

    # Sendgrid has a 30 MB limit on everything, this estimate should be slightly stricter
    size = (
        len(content_html or "")
        + len(content_text or "")
        + sum([len(att.content_base64) for att in attachments])
    )
    max = 30 * 1024**2  # 30 MB
    headroom = 100 * 1024  # leave some room for headers etc
    if size > max - headroom:
        raise ValueError(
            "Email and attachment size exceeds 30MB, please reduce the size of the email."
        )

    return Email(
        to=validate_email_to_arg(to),
        subject=subject,
        content_text=content_text,
        content_html=content_html,
        attachments=attachments,
    )


def email(
    to: Union[str, List[str]],
    subject: str,
    *,
    content_text: Optional[str] = None,
    content_html: Optional[str] = None,
    attachments: Sequence[Attachment] = (),
):
    """Send email notification from databutton.

    At least one of the content arguments must be present.

    A link to the project will be added at the end of the email body.

    If content_text is not provided it will be generated from
    content_html for email clients without html support,
    the result may be less pretty than handcrafted text.
    """
    send(
        create_email(
            to=to,
            subject=subject,
            content_text=content_text,
            content_html=content_html,
            attachments=attachments,
        )
    )
