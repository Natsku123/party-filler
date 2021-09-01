from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class OAuth2Token(SQLModel, table=True):
    token_id: int = Field(
        sa_column=Column(Integer, primary_key=True, nullable=False),
        alias="tokenId",
        description="ID of token",
    )
    player_id: int = Field(
        sa_column=Column(Integer, ForeignKey("player.id"), nullable=False),
        gt=0,
        alias="playerId",
        description="ID of player",
    )
    name: str = Field(
        sa_column=Column(String(20), nullable=False),
        description="Name of token OAuth provider",
    )

    player: "Player" = Relationship(sa_relationship=relationship("Player"))

    token_type: Optional[str] = Field(
        sa_column=Column(String(20)), alias="tokenType", description="Type of token"
    )
    access_token: str = Field(
        sa_column=Column(String(48), nullable=False),
        alias="accessToken",
        description="Access token from OAuth provider",
    )
    refresh_token: Optional[str] = Field(
        sa_column=Column(String(48)),
        alias="refreshToken",
        description="Refresh token from OAuth provider",
    )
    expires_at: Optional[int] = Field(
        sa_column=Column(Integer, default=0),
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
