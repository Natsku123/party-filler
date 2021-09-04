from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from .models import Player


class OAuth2Token(SQLModel):
    token_id: int = Field(
        alias="tokenId",
        description="ID of token",
    )
    player_id: int = Field(
        gt=0,
        alias="playerId",
        description="ID of player",
    )
    name: str = Field(
        description="Name of token OAuth provider",
    )

    player: "Player"

    token_type: Optional[str] = Field(alias="tokenType", description="Type of token")
    access_token: str = Field(
        alias="accessToken",
        description="Access token from OAuth provider",
    )
    refresh_token: Optional[str] = Field(
        alias="refreshToken",
        description="Refresh token from OAuth provider",
    )
    expires_at: Optional[int] = Field(
        ge=0,
        alias="expiresAt",
        description="Token expiration",
    )

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OAuth2TokenCreate(SQLModel):
    player_id: int = Field(gt=0, alias="playerId", description="ID of player")
    name: str = Field(description="Name of token OAuth provider")
    token_type: Optional[str] = Field(
        None, alias="tokenType", description="Type of token"
    )
    access_token: str = Field(
        alias="accessToken", description="Access token from OAuth provider"
    )
    refresh_token: Optional[str] = Field(
        None, alias="refreshToken", description="Refresh token from OAuth provider"
    )
    expires_at: Optional[int] = Field(
        0, ge=0, alias="expiresAt", description="Token expiration"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OAuth2TokenUpdate(SQLModel):
    player_id: Optional[int] = Field(
        None, gt=0, alias="playerId", description="ID of player"
    )
    name: Optional[str] = Field(None, description="Name of token OAuth provider")
    token_type: Optional[str] = Field(
        None, alias="tokenType", description="Type of token"
    )
    access_token: Optional[str] = Field(
        None, alias="accessToken", description="Access token from OAuth provider"
    )
    refresh_token: Optional[str] = Field(
        None, alias="refreshToken", description="Refresh token from OAuth provider"
    )
    expires_at: Optional[int] = Field(
        None, ge=0, alias="expiresAt", description="Token expiration"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OAuth2TokenShort(SQLModel):
    token_id: int = Field(alias="tokenId", description="ID of token")
    player_id: int = Field(gt=0, alias="playerId", description="ID of player")
    name: str = Field(description="Name of token OAuth provider")
    token_type: Optional[str] = Field(
        None, alias="tokenType", description="Type of token"
    )
    access_token: str = Field(
        alias="accessToken", description="Access token from OAuth provider"
    )
    refresh_token: Optional[str] = Field(
        None, alias="refreshToken", description="Refresh token from OAuth provider"
    )
    expires_at: Optional[int] = Field(
        0, ge=0, alias="expiresAt", description="Token expiration"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
