from .channels import Channel, ChannelRead, ChannelShort, ChannelCreate, ChannelUpdate
from .games import Game, GameRead, GameShort, GameCreate, GameUpdate
from .members import Member, MemberRead, MemberShort, MemberCreate, MemberUpdate
from .oauth import OAuth2Token, OAuth2TokenShort, OAuth2TokenCreate, OAuth2TokenUpdate
from .parties import Party, PartyRead, PartyShort, PartyCreate, PartyUpdate
from .players import Player, PlayerRead, PlayerShort, PlayerCreate, PlayerUpdate
from .roles import Role, RoleRead, RoleShort, RoleCreate, RoleUpdate
from .servers import Server, ServerRead, ServerShort, ServerCreate, ServerUpdate

Channel.update_forward_refs()
ChannelRead.update_forward_refs(ServerShort=ServerShort)
ChannelShort.update_forward_refs()

Game.update_forward_refs()
GameRead.update_forward_refs()
GameShort.update_forward_refs()

Member.update_forward_refs()
MemberRead.update_forward_refs(
    PartyShort=PartyShort, PlayerShort=PlayerShort, RoleShort=RoleShort
)
MemberShort.update_forward_refs(PlayerShort=PlayerShort, RoleShort=RoleShort)

OAuth2Token.update_forward_refs()
OAuth2TokenShort.update_forward_refs()

Party.update_forward_refs()
PartyRead.update_forward_refs(
    ChannelShort=ChannelShort,
    PlayerShort=PlayerShort,
    MemberShort=MemberShort,
    RoleShort=RoleShort,
    GameShort=GameShort,
)
PartyShort.update_forward_refs()

Player.update_forward_refs()
PlayerRead.update_forward_refs(ServerShort=ServerShort)
PlayerShort.update_forward_refs()

Role.update_forward_refs()
RoleRead.update_forward_refs(PartyShort=PartyShort)
RoleShort.update_forward_refs()

Server.update_forward_refs()
ServerRead.update_forward_refs(ChannelShort=ChannelShort, PlayerShort=PlayerShort)
ServerShort.update_forward_refs()
