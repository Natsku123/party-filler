from typing import List, Optional
from pydantic import BaseModel, Field


class OAuth2TokenBase(BaseModel):
    player_id: int = Field(
        ...,
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
        alias="expiresAt",
        description="Token expiration"
    )


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


class MemberBase(BaseModel):
    party_id: int = Field(
        ...,
        alias="partyId",
        description="ID of party"
    )
    player_id: int = Field(
        ...,
        alias="playerId",
        description="ID of player"
    )
    role_id: Optional[int] = Field(
        None,
        alias="roleId",
        description="ID of role"
    )
    player_req: Optional[int] = Field(
        None,
        alias="playerReq",
        description="Required number of players for member to play"
    )


class PartyBase(BaseModel):
    title: str = Field(
        ...,
        description="Title of party"
    )
    leader_id: int = Field(
        ...,
        alias="leaderId",
        description="ID of party leader"
    )
    game_id: int = Field(
        ...,
        alias="gameId",
        description="ID of game to be played"
    )
    max_players: Optional[int] = Field(
        None,
        alias="maxPlayers",
        description="Maximum number of players"
    )
    min_players: Optional[int] = Field(
        None,
        alias="minPlayers",
        description="Minimum number of players"
    )
    description: Optional[str] = Field(
        "",
        description="Description of party"
    )
    channel_id: Optional[int] = Field(
        None,
        alias="channelId",
        description="ID of channel"
    )
    start_time: Optional[str] = Field(
        None,
        alias="startTime",
        description="Party search start time"
    )
    end_time: Optional[str] = Field(
        None,
        alias="endTime",
        description="Party search end time"
    )


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


class RoleBase(BaseModel):
    party_id: Optional[int] = Field(
        None,
        alias="partyId",
        description="ID of party"
    )
    name: Optional[str] = Field(
        None,
        description="Name of role"
    )
    max_players: Optional[int] = Field(
        None,
        alias="maxPlayers",
        description="Maximum number of players of role"
    )


class GameBase(BaseModel):
    name: str = Field(
        ...,
        description="Name of game"
    )
    default_max_players: Optional[int] = Field(
        None,
        alias="defaultMaxPlayers",
        description="Default number of maximum players for this game"
    )


class OAuth2TokenCreate(OAuth2TokenBase):
    pass


class PlayerCreate(PlayerBase):
    pass


class MemberCreate(MemberBase):
    pass


class PartyCreate(PartyBase):
    pass


class ChannelCreate(ChannelBase):
    pass


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
    player: 'Player' = Field(
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
    servers: List['Server'] = Field(
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
    party: 'Party' = Field(
        ...,
        description="Party object"
    )
    player: Player = Field(
        ...,
        description="Player object"
    )
    role: Optional['Role'] = Field(
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
    leader: Player = Field(
        ...,
        description="Player object of leader"
    )
    members: List[Member] = Field(
        [],
        description="Member objects of party"
    )
    game: 'Game' = Field(
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

    class Config:
        orm_mode = True


class Server(ServerBase):
    id: int = Field(
        ...,
        description="ID of server"
    )
    channels: List[Channel] = Field(
        [],
        description="Channel objects"
    )
    players: List[Player] = Field(
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
    party: Optional[Party] = Field(
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


OAuth2Token.update_forward_refs()
Player.update_forward_refs()
Member.update_forward_refs()
Party.update_forward_refs()
Channel.update_forward_refs()
Server.update_forward_refs()
Role.update_forward_refs()
Game.update_forward_refs()
