import base64
import mimetypes
import re
from collections.abc import Sequence
from typing import List, Optional, Union

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

    # Filename
    name: Optional[str] = None

    # MIME type of the attachment
    type: Optional[str] = None

    # ID to use for inline attachments
    cid: Optional[str] = None

    # Base64 encoded data
    base64_content: str


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


def create_attachment(
    *,
    content: bytes | str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    cid: Optional[str] = None,
) -> Attachment:
    """Create an attachment to be included with an email.

    Content can either be a string or a bytes object.
    We will base64 encode it for you.

    The content type can be omitted if the name has a normal file extension.

    To use an attachment as an inline image in the email,
    set the `cid="my_image_id"` parameter,
    and use `<img src="cid:my_image_id">` in the html content.
    """
    return Attachment(
        name=name,
        type=determine_type(type, name),
        base64_content=encode_content(content),
        cid=cid,
    )


def validate_attachment(att: Attachment) -> Attachment:
    assert isinstance(att, Attachment)
    assert att.type
    assert att.name
    assert att.base64_content
    assert isinstance(att.base64_content, str)
    assert re.match(r"^[A-Za-z0-9+/=]+$", att.base64_content)
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
        + sum([len(att.base64_content) for att in attachments])
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
