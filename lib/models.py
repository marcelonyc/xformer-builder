from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    UrlConstraints,
    AfterValidator,
    AnyUrl,
)
from pydantic.types import List, Any, Annotated
from pydantic.networks import Url
from typing import Optional
from enum import Enum
from typing_extensions import Self
from datetime import datetime, timezone
import iso8601
from config.app_config import get_settings


class XformerRow(BaseModel):
    name: str
    column_index: int
    column_type: str
    code: Any
    sample: Any
    target_type: Annotated[str, Field(validate_default=True)] = ""
    target_column: Annotated[str, Field(validate_default=True)] = ""
    target_sample: Annotated[str, Field(validate_default=True)] = ""

    @model_validator(mode="after")
    def is_nonee(self) -> Self:

        if self.target_type == "":
            self.target_type = self.column_type
        if self.target_column == "":
            self.target_column = self.name
        if self.target_sample == "":
            self.target_sample = self.sample
        return self


class XformerLists(BaseModel):
    # List elements of xformer
    source_column: List
    code: List
    source_type: List
    target_type: List
    target_column: List
    sample: List


class XformerData(BaseModel):
    # Read get xformer response
    id: Optional[str] = None
    name: str
    description: str
    xformer: XformerLists


class Xformer(BaseModel):
    # Payload for saving xformer
    name: str = None
    description: str = None
    update: bool = False
    xformer: XformerLists


class XformerAllRows(BaseModel):
    rows: List[XformerData]


class XformerAssociationResponse(BaseModel):
    file_id: str


class XformerAssociationPayload(BaseModel):
    xformer_id: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    failed_event_trigger_id: Optional[str] = None
    success_event_trigger_id: Optional[str] = None


class UploadedFilesResponse(BaseModel):
    file_id: str
    upload_id: str
    file_size: int
    upload_date: str
    last_update_message: str
    description: Optional[str]
    file_ttl: int = 0
    file_expires_in_hours: Annotated[int, Field(validate_default=True)] = 0

    @model_validator(mode="after")
    def update_expiration(self) -> Self:
        if self.file_ttl != 0:
            _uploaded = iso8601.parse_date(self.upload_date)
            _now = datetime.now(timezone.utc)
            _date_diff = round((_now - _uploaded).total_seconds() / 3600)
            self.file_expires_in_hours = self.file_ttl - _date_diff
            if self.file_expires_in_hours == 0:
                self.file_expires_in_hours = self.file_ttl

        return self


class ListUploadedFilesResponse(BaseModel):
    files: List[UploadedFilesResponse]


class EventTriggerTypes(str, Enum):
    webhook = "webhook"
    # email = "email"


class EventTriggerPayload(BaseModel):
    id: str
    event_description: str
    event_type: EventTriggerTypes


class EventTriggerResponse(BaseModel):
    id: str
    user_id: str
    event_description: str
    event_type: EventTriggerTypes
    event_meta: Any


class EventTriggerList(BaseModel):
    triggers: List[EventTriggerResponse]


class WebHookMethods(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


class WebhookEventMetadata(EventTriggerPayload):

    def check_allowed_hosts(url: AnyUrl) -> AnyUrl:
        allowed_urls = get_settings().webhook_domain_whitelist

        if url.host in allowed_urls and url.scheme in {"http", "https"}:
            return url
        raise ValueError("It's not in the list of accepted hosts")

    url: Annotated[Url, AfterValidator(check_allowed_hosts)]
    method: WebHookMethods
    headers: Optional[dict]
    body: Optional[str]


class EmailEventMetadata(EventTriggerPayload):
    to: str
    subject: str
    body: str
