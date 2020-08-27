import dateutil
from sqlalchemy.orm import Session
from . import models, schemas


def get_parties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Party).order_by(models.Party.id.desc())\
        .offset(skip).limit(limit).all()


def get_party(db: Session, party_id: int):
    return db.query(models.Party).filter(
        models.Party.id == party_id
    ).first()


def create_party(db: Session, party: schemas.PartyCreate):
    start_time = None
    end_time = None

    if party.start_time:
        start_time = dateutil.parser.parse(party.start_time)

    if party.end_time:
        end_time = dateutil.parser.parse(party.end_time)

    db_party = models.Party(
        title=party.title,
        leader_id=party.leader_id,
        game_id=party.game_id,
        max_players=party.max_players,
        min_players=party.min_players,
        description=party.description,
        channel_id=party.channel_id,
        start_time=start_time,
        end_time=end_time
    )

    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party


def delete_party(db: Session, party_id: int):
    party = db.query(models.Party).filter(
        models.Party.id == party_id
    ).first()
    db.delete(party)
    db.commit()
    return party


def update_party(db: Session, party: schemas.Party):
    start_time = None
    end_time = None

    if party.start_time:
        start_time = dateutil.parser.parse(party.start_time)

    if party.end_time:
        end_time = dateutil.parser.parse(party.end_time)

    db_party = db.query(models.Party).filter(
        models.Party.id == party.id
    ).first()

    db_party.title = party.title
    db_party.leader_id = party.leader_id
    db_party.game = party.game
    db_party.max_players = party.max_players
    db_party.min_players = party.min_players
    db_party.description = party.description
    db_party.channel_id = party.channel_id
    db_party.start_time = start_time
    db_party.end_time = end_time

    db.commit()
    db.refresh(db_party)

    return db_party


def get_server(db: Session, server_id: int):
    return db.query(models.Server).filter(
        models.Server.id == server_id
    ).first()


def get_servers(db: Session):
    return db.query(models.Server).order_by(models.Server.name.asc()).all()


def create_server(db: Session, server: schemas.ServerCreate):
    db_server = models.Server(**server.dict())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


def delete_server(db: Session, server_id: int):
    server = db.query(models.Server).filter(
        models.Server.id == server_id
    ).first()

    db.delete(server)
    db.commit()
    return server


def update_server(db: Session, server: schemas.Server):
    db_server = db.query(models.Server).filter(
        models.Server.id == server.id
    ).first()

    db_server.name = server.name
    db_server.icon = server.icon
    db_server.discord_id = server.discord_id

    db.commit()
    db.refresh(db_server)
    return db_server


def get_channel(db: Session, channel_id: int):
    return db.query(models.Channel).filter(
        models.Channel.id == channel_id
    ).first()


def get_channels(db: Session):
    return db.query(models.Channel).order_by(models.Channel.name.asc()).all()


def create_channel(db: Session, channel: schemas.ChannelCreate):
    db_channel = models.Channel(**channel.dict())

    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


def update_channel(db: Session, channel: schemas.Channel):
    db_channel = db.query(models.Channel).filter(
        models.Channel.id == channel.id
    ).first()

    db_channel.name = channel.name
    db_channel.discord_id = channel.discord_id
    db_channel.server_id = channel.server_id

    db.commit()
    db.refresh(db_channel)
    return db_channel


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.id == player_id
    ).first()


def get_players(db: Session):
    return db.query(models.Player).order_by(models.Player.name.asc()).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(**player.dict())

    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player: schemas.Player):
    db_player = db.query(models.Player).filter(
        models.Player.id == player.id
    ).first()

    db_player.name = player.name
    db_player.discriminator = player.discriminator
    db_player.discord_id = player.discord_id
    db_player.icon = player.icon

    db.commit()
    db.refresh(db_player)

    return db_player


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(
        models.Member.id == member_id
    ).first()


def get_members(db: Session):
    return db.query(models.Member).order_by(models.Member.id.asc()).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


def update_member(db: Session, member: schemas.Member):
    db_member = db.query(models.Member).filter(
        models.Member.id == member.id
    ).first()

    db_member.party_id = member.party_id
    db_member.player_id = member.player_id
    db_member.role_id = member.role_id
    db_member.player_req = member.player_req

    db.commit()
    db.refresh(db_member)

    return db_member


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(
        models.Role.id == role_id
    ).first()


def get_roles(db: Session):
    return db.query(models.Role).order_by(models.Role.party_id.asc())


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role


def update_role(db: Session, role: schemas.Role):
    db_role = db.query(models.Role).filter(
        models.Role.id == role.id
    ).first()

    db_role.party_id = role.party_id
    db_role.name = role.name
    db_role.max_players = role.max_players

    db.commit()
    db.refresh(db_role)

    return db_role


def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(
        models.Game.id == game_id
    ).first()


def get_games(db: Session):
    return db.query(models.Game).order_by(models.Game.name.asc()).all()


def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(**game.dict())

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def update_game(db: Session, game: schemas.Game):
    db_game = db.query(models.Game).filter(
        models.Game.id == game.id
    ).first()

    db_game.name = game.name
    db_game.default_max_players = game.default_max_players

    db.commit()
    db.refresh(db_game)

    return db_game


def get_server_channel(db: Session, server_id: int):
    return db.query(models.Channel).filter(
        models.Channel.server_id == server_id
    ).all()


def get_party_members(db: Session, party_id: int):
    return db.query(models.Member).filter(
        models.Member.party_id == party_id
    ).all()
