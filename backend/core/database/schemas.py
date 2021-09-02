from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .members import MemberRead
    from .channels import ChannelRead
    from .parties import PartyRead


class Meta(SQLModel):
    version: Optional[str]
    build: Optional[str]


class WebhookEvent(SQLModel):
    name: str = (Field(..., description="Name / identifier of event"),)
    timestamp: Optional[datetime] = Field(None, description="Timestamp")

    class Config:
        allow_population_by_field_name = True


class MemberJoinWebhook(SQLModel):
    member: "MemberRead" = (Field(..., description="Member that joined"),)
    channel: "ChannelRead" = (Field(..., description="Channel to notify"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyCreateWebhook(SQLModel):
    party: "PartyRead" = (Field(..., description="Party created"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyFullWebhook(SQLModel):
    party: "PartyRead" = (Field(..., description="Party filled"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyReadyWebhook(SQLModel):
    party: "PartyRead" = (Field(..., description="Party that is ready"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyTimedoutWebhook(SQLModel):
    party: "PartyRead" = (Field(..., description="Party that timed out"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class IsSuperUser(SQLModel):
    is_superuser: bool = Field(
        ..., alias="isSuperuser", description="Is current user superuser"
    )
