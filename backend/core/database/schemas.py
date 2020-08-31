from typing import List, Optional
from pydantic import BaseModel


class OAuth2TokenBase(BaseModel):
    player_id: int
    name: str
    token_type: Optional[str] = None
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = 0


class PlayerBase(BaseModel):
    name: str
    discriminator: str
    discord_id: str
    icon: Optional[str] = None


class MemberBase(BaseModel):
    party_id: int
    player_id: int
    role_id: Optional[int] = None
    player_req: Optional[int] = None


class PartyBase(BaseModel):
    title: str
    leader_id: int
    game_id: int
    max_players: Optional[int] = None
    min_players: Optional[int] = None
    description: Optional[str] = ""
    channel_id: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class ChannelBase(BaseModel):
    name: str
    discord_id: str
    server_id: int


class ServerBase(BaseModel):
    name: str
    icon: Optional[str] = None
    discord_id: str


class RoleBase(BaseModel):
    party_id: Optional[int] = None
    name: Optional[str] = None
    max_players: Optional[int] = None


class GameBase(BaseModel):
    name: str
    default_max_players: Optional[int] = None


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
    token_id: int
    player: 'Player'

    class Config:
        orm_mode = True


class Player(PlayerBase):
    id: int
    servers: List['Server'] = []

    class Config:
        orm_mode = True


class Member(MemberBase):
    id: int
    party: 'Party'
    player: Player
    role: 'Role'

    class Config:
        orm_mode = True


class Party(PartyBase):
    id: int
    channel: 'Channel'
    leader: Player
    members: List[Member] = []
    game: 'Game'

    class Config:
        orm_mode = True


class Channel(ChannelBase):
    id: int

    class Config:
        orm_mode = True


class Server(ServerBase):
    id: int
    channels: List[Channel] = []
    players: List[Player] = []

    class Config:
        orm_mode = True


class Role(RoleBase):
    id: int
    party: Party

    class Config:
        orm_mode = True


class Game(GameBase):
    id: int

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
