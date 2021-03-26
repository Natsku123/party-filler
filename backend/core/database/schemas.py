from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator, root_validator


class OAuth2TokenBase(BaseModel):
    player_id: int = Field(
        ...,
        gt=0,
        alias="playerId",
        description="ID of player"
    )
    name: str = Field(
        ...,
        description="Name of token OAuth provider"
    )
    token_type: Optional[str] = Field(
        None,
        alias="tokenType",
        description="Type of token"
    )
    access_token: str = Field(
        ...,
        alias="accessToken",
        description="Access token from OAuth provider"
    )
    refresh_token: Optional[str] = Field(
        None,
        alias="refreshToken",
        description="Refresh token from OAuth provider"
    )
    expires_at: Optional[int] = Field(
        0,
        ge=0,
        alias="expiresAt",
        description="Token expiration"
    )

    class Config:
        allow_population_by_field_name = True


class PlayerBase(BaseModel):
    name: str = Field(
        ...,
        description="Discord username of player"
    )
    discriminator: str = Field(
        ...,
        description="Discord user discriminator"
    )
    discord_id: str = Field(
        ...,
        alias="discordId",
        description="ID on discord"
    )
    icon: Optional[str] = Field(
        None,
        description="Discord icon hash"
    )

    class Config:
        allow_population_by_field_name = True


class MemberBase(BaseModel):
    party_id: int = Field(
        ...,
        gt=0,
        alias="partyId",
        description="ID of party"
    )
    player_id: int = Field(
        ...,
        gt=0,
        alias="playerId",
        description="ID of player"
    )
    role_id: Optional[int] = Field(
        None,
        gt=0,
        alias="roleId",
        description="ID of role"
    )
    player_req: Optional[int] = Field(
        None,
        gt=0,
        alias="playerReq",
        description="Required number of players for member to play"
    )

    class Config:
        allow_population_by_field_name = True


class PartyBase(BaseModel):
    title: str = Field(
        ...,
        description="Title of party"
    )
    leader_id: int = Field(
        ...,
        gt=0,
        alias="leaderId",
        description="ID of party leader"
    )
    game_id: int = Field(
        ...,
        gt=0,
        alias="gameId",
        description="ID of game to be played"
    )
    max_players: Optional[int] = Field(
        None,
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players"
    )
    min_players: Optional[int] = Field(
        None,
        gt=0,
        alias="minPlayers",
        description="Minimum number of players"
    )
    description: Optional[str] = Field(
        "",
        description="Description of party"
    )
    channel_id: Optional[int] = Field(
        None,
        gt=0,
        alias="channelId",
        description="ID of channel"
    )
    start_time: Optional[datetime] = Field(
        None,
        alias="startTime",
        description="Party search start time"
    )
    end_time: Optional[datetime] = Field(
        None,
        alias="endTime",
        description="Party search end time"
    )

    @root_validator
    def check_min_and_max_players(cls, values):
        min_p, max_p = values.get('min_players'), values.get('max_players')
        if min_p > max_p:
            raise ValueError("Maximum number of players cannot "
                             "be less than the minimum!")
        return values

    @root_validator
    def check_times(cls, values):
        start, end = values.get('start_time'), values.get('end_time')
        if start > end:
            raise ValueError("Start time cannot be greater than end time")

        return values

    @validator('start_time')
    def check_start_time(cls, v):
        delta = (datetime.now() - v)
        if delta.minute > 30:
            raise ValueError("Start time cannot be more than 30 "
                             "minutes apart from current time")
        return v

    @validator('end_time')
    def check_end_time(cls, v):
        now = datetime.now()
        if now > v:
            raise ValueError("End time cannot be less than current time")
        return v

    class Config:
        allow_population_by_field_name = True


class ChannelBase(BaseModel):
    name: str = Field(
        ...,
        description="Name of channel from Discord"
    )
    discord_id: str = Field(
        ...,
        alias="discordId",
        description="Discord ID of channel"
    )
    server_id: int = Field(
        ...,
        alias="serverId",
        description="ID of server associated with"
    )

    class Config:
        allow_population_by_field_name = True


class ServerBase(BaseModel):
    name: str = Field(
        ...,
        description="Name of server from Discord"
    )
    icon: Optional[str] = Field(
        None,
        description="Icon of server from Discord"
    )
    discord_id: str = Field(
        ...,
        alias="discordId",
        description="Discord ID of server"
    )

    class Config:
        allow_population_by_field_name = True


class RoleBase(BaseModel):
    party_id: Optional[int] = Field(
        None,
        gt=0,
        alias="partyId",
        description="ID of party"
    )
    name: Optional[str] = Field(
        None,
        description="Name of role"
    )
    max_players: Optional[int] = Field(
        None,
        gt=0,
        alias="maxPlayers",
        description="Maximum number of players of role"
    )

    class Config:
        allow_population_by_field_name = True


class GameBase(BaseModel):
    name: str = Field(
        ...,
        description="Name of game"
    )
    default_max_players: Optional[int] = Field(
        None,
        gt=0,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game"
    )

    class Config:
        allow_population_by_field_name = True


class OAuth2TokenCreate(OAuth2TokenBase):
    pass


class PlayerCreate(PlayerBase):
    pass


class MemberCreate(MemberBase):
    pass


class PartyCreate(PartyBase):
    pass


class ChannelCreate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Name of channel from Discord"
    )
    discord_id: str = Field(
        ...,
        alias="discordId",
        description="Discord ID of channel"
    )
    server_id: Optional[int] = Field(
        None,
        alias="serverId",
        description="ID of server associated with"
    )

    class Config:
        allow_population_by_field_name = True


class ServerCreate(ServerBase):
    pass


class RoleCreate(RoleBase):
    pass


class GameCreate(GameBase):
    pass


class OAuth2TokenUpdate(OAuth2TokenBase):
    pass


class PlayerUpdate(PlayerBase):
    pass


class MemberUpdate(MemberBase):
    pass


class PartyUpdate(PartyBase):
    pass


class ChannelUpdate(ChannelBase):
    pass


class ServerUpdate(ServerBase):
    pass


class RoleUpdate(RoleBase):
    pass


class GameUpdate(GameBase):
    pass


class OAuth2Token(OAuth2TokenBase):
    token_id: int = Field(
        ...,
        alias="tokenId",
        description="ID of token"
    )
    player: 'PlayerShort' = Field(
        ...,
        description="Player object"
    )

    class Config:
        orm_mode = True


class Player(PlayerBase):
    id: int = Field(
        ...,
        description="ID of player"
    )
    servers: List['ServerShort'] = Field(
        [],
        description="List of server objects player is on"
    )

    class Config:
        orm_mode = True


class Member(MemberBase):
    id: int = Field(
        ...,
        description="ID of member"
    )
    party: 'PartyShort' = Field(
        ...,
        description="Party object"
    )
    player: 'PlayerShort' = Field(
        ...,
        description="Player object"
    )
    role: Optional['RoleShort'] = Field(
        None,
        description="Role object"
    )

    class Config:
        orm_mode = True


class Party(PartyBase):
    id: int = Field(
        ...,
        description="ID of party"
    )
    channel: Optional['Channel'] = Field(
        None,
        description="Channel object"
    )
    leader: 'PlayerShort' = Field(
        ...,
        description="Player object of leader"
    )
    members: List['MemberShort'] = Field(
        [],
        description="Member objects of party"
    )
    game: 'GameShort' = Field(
        None,
        description="Game object"
    )

    class Config:
        orm_mode = True


class Channel(ChannelBase):
    id: int = Field(
        ...,
        description="ID of channel"
    )
    server: 'ServerShort' = Field(
        ...,
        description="Server of channel"
    )

    class Config:
        orm_mode = True


class Server(ServerBase):
    id: int = Field(
        ...,
        description="ID of server"
    )
    channels: List['ChannelShort'] = Field(
        [],
        description="Channel objects"
    )
    players: List['PlayerShort'] = Field(
        [],
        description="Players objects"
    )

    class Config:
        orm_mode = True


class Role(RoleBase):
    id: int = Field(
        ...,
        description="ID of role"
    )
    party: Optional['PartyShort'] = Field(
        None,
        description="Party object"
    )

    class Config:
        orm_mode = True


class Game(GameBase):
    id: int = Field(
        ...,
        description="ID of game"
    )

    class Config:
        orm_mode = True


class OAuth2TokenShort(OAuth2TokenBase):
    token_id: int = Field(
        ...,
        alias="tokenId",
        description="ID of token"
    )

    class Config:
        orm_mode = True


class PlayerShort(PlayerBase):
    id: int = Field(
        ...,
        description="ID of player"
    )

    class Config:
        orm_mode = True


class MemberShort(MemberBase):
    id: int = Field(
        ...,
        description="ID of member"
    )

    class Config:
        orm_mode = True


class PartyShort(PartyBase):
    id: int = Field(
        ...,
        description="ID of party"
    )

    class Config:
        orm_mode = True


class ChannelShort(ChannelBase):
    id: int = Field(
        ...,
        description="ID of channel"
    )

    class Config:
        orm_mode = True


class ServerShort(ServerBase):
    id: int = Field(
        ...,
        description="ID of server"
    )

    class Config:
        orm_mode = True


class RoleShort(RoleBase):
    id: int = Field(
        ...,
        description="ID of role"
    )

    class Config:
        orm_mode = True


class GameShort(GameBase):
    id: int = Field(
        ...,
        description="ID of game"
    )

    class Config:
        orm_mode = True


OAuth2Token.update_forward_refs()
Player.update_forward_refs()
Member.update_forward_refs()
Party.update_forward_refs()
Channel.update_forward_refs()
Server.update_forward_refs()
Role.update_forward_refs()
Game.update_forward_refs()


class WebhookEvent(BaseModel):
    name: str = Field(
        ...,
        description="Name / identifier of event"
    ),
    timestamp: Optional[datetime] = Field(
        None,
        description="Timestamp"
    )

    class Config:
        allow_population_by_field_name = True


class MemberJoinWebhook(BaseModel):
    member: 'Member' = Field(
        ...,
        description="Member that joined"
    ),
    channel: 'Channel' = Field(
        ...,
        description="Channel to notify"
    ),
    event: 'WebhookEvent' = Field(
        ...,
        description="Event info"
    )


class PartyCreateWebhook(BaseModel):
    party: 'Party' = Field(
        ...,
        description="Party created"
    ),
    event: 'WebhookEvent' = Field(
        ...,
        description="Event info"
    )


class IsSuperUser(BaseModel):
    is_superuser: bool = Field(
        ...,
        alias="isSuperuser",
        description="Is current user superuser"
    )
