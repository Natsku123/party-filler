from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Meta(BaseModel):
    version: Optional[str]
    build: Optional[str]


class WebhookEvent(BaseModel):
    name: str = (Field(..., description="Name / identifier of event"),)
    timestamp: Optional[datetime] = Field(None, description="Timestamp")

    class Config:
        allow_population_by_field_name = True


class MemberJoinWebhook(BaseModel):
    member: "Member" = (Field(..., description="Member that joined"),)
    channel: "Channel" = (Field(..., description="Channel to notify"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyCreateWebhook(BaseModel):
    party: "Party" = (Field(..., description="Party created"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyFullWebhook(BaseModel):
    party: "Party" = (Field(..., description="Party filled"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyReadyWebhook(BaseModel):
    party: "Party" = (Field(..., description="Party that is ready"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class PartyTimedoutWebhook(BaseModel):
    party: "Party" = (Field(..., description="Party that timed out"),)
    event: "WebhookEvent" = Field(..., description="Event info")


class IsSuperUser(BaseModel):
    is_superuser: bool = Field(
        ..., alias="isSuperuser", description="Is current user superuser"
    )
