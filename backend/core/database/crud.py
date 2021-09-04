import dateutil.parser
import json
from sqlmodel import SQLModel, Session, asc, desc, col, select, func

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core.utils import camel_dict_to_snake

from core.database import models

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

FilterParseException = HTTPException(
    status_code=400, detail="Filter parsing failed. Invalid attributes present."
)

OrderParseException = HTTPException(
    status_code=400, detail="Order parsing failed. Invalid attributes present."
)

JSONParseError = HTTPException(status_code=400, detail="Invalid JSON string")


def parse_filter(filters: dict, parent: Any) -> list:
    """
    Convert filter dict into filter list

    :param filters: Dict to be converted
    :param parent: Parent object / model
    :return: Filter list
    """
    new_filters = []

    for k, v in filters.items():

        # Detect comparison
        gt = "__gt" in k
        ge = "__ge" in k
        lt = "__lt" in k
        le = "__le" in k

        # Remove suffixes
        if gt or ge or lt or le:
            k = k[:-4]

        try:
            attr = getattr(parent, k)

            # Construct filter expressions
            if isinstance(v, dict):
                new_filters += parse_filter(v, attr.property.mapper.class_)
            else:
                if gt:
                    new_filters.append(col(attr) > v)
                elif ge:
                    new_filters.append(col(attr) >= v)
                elif lt:
                    new_filters.append(col(attr) < v)
                elif le:
                    new_filters.append(col(attr) <= v)
                else:
                    new_filters.append(col(attr) == v)
        except AttributeError:
            raise FilterParseException

    return new_filters


def parse_order(order: List[str], parent) -> List[str]:
    """
    Convert order list into usable version in SQLAlchemy

    :param order: Order list
    :param parent: Parent object
    :return: New order list
    """
    for i, v in enumerate(order):
        a = "__a" in v
        d = "__d" in v

        if a or d:
            v = v[:-3]

        if not hasattr(parent, v):
            raise OrderParseException

        order[i] = (
            asc(col(getattr(parent, v)))
            if a and not d
            else desc(col(getattr(parent, v)))
            if not a and d
            else col(getattr(parent, v))
        )
    return order


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_count(self, db: Session) -> int:
        """
        Get total number of objects in database.
        :param db: Database Session to be used
        """
        # return db.query(self.model).count()
        return db.scalar(select(func.count()).select_from(self.model))

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        # return db.query(self.model).filter(self.model.id == id).first()
        return db.exec(select(self.model).filter(self.model.id == id)).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Union[Dict, str]] = None,
        group: Optional[Union[List[str], str]] = None,
        order: Optional[Union[List[str], str]] = None
    ) -> List[ModelType]:

        q = select(self.model)

        # Add filter to query
        if filters is not None:
            if isinstance(filters, str):
                try:
                    filters = json.loads(filters)
                except json.decoder.JSONDecodeError:
                    raise JSONParseError

                if not isinstance(filters, dict):
                    raise JSONParseError

            q = q.filter(*parse_filter(filters, self.model))

        # Add grouping to query
        if group is not None:
            if isinstance(group, str):
                try:
                    group = json.loads(group)
                except json.decoder.JSONDecodeError:
                    raise JSONParseError

                if not isinstance(group, list):
                    raise JSONParseError

            q = q.group_by(*group)

        # Add ordering to query
        if order is not None:
            if isinstance(order, str):
                try:
                    order = json.loads(order)
                except json.decoder.JSONDecodeError:
                    raise JSONParseError
                if not isinstance(order, list):
                    raise JSONParseError

            q = q.order_by(*parse_order(order, self.model))

        return db.exec(q.offset(skip).limit(limit)).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = camel_dict_to_snake(jsonable_encoder(obj_in))
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = camel_dict_to_snake(jsonable_encoder(db_obj))

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDParty(CRUDBase[models.Party, models.PartyCreate, models.PartyUpdate]):
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = camel_dict_to_snake(jsonable_encoder(obj_in))
        start_time = None
        end_time = None

        if "start_time" in obj_in_data and obj_in_data["start_time"]:
            start_time = dateutil.parser.parse(obj_in_data["start_time"])

        if "end_time" in obj_in_data and obj_in_data["end_time"]:
            end_time = dateutil.parser.parse(obj_in_data["end_time"])

        db_party = models.Party(
            title=obj_in_data["title"],
            leader_id=obj_in_data["leader_id"],
            game_id=obj_in_data["game_id"],
            max_players=obj_in_data["max_players"],
            min_players=obj_in_data["min_players"],
            description=obj_in_data["description"],
            channel_id=obj_in_data["channel_id"],
            start_time=start_time,
            end_time=end_time,
        )

        db.add(db_party)
        db.commit()
        db.refresh(db_party)
        return db_party

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = camel_dict_to_snake(jsonable_encoder(db_obj))

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if (
                field in update_data
                and field == "start_time"
                and isinstance(update_data["start_time"], str)
            ):
                setattr(db_obj, field, dateutil.parser.parse(update_data["start_time"]))
            elif (
                field in update_data
                and field == "end_time"
                and isinstance(update_data["end_time"], str)
            ):
                setattr(db_obj, field, dateutil.parser.parse(update_data["end_time"]))
            elif field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def lock(self, db: Session, *, db_obj: ModelType) -> ModelType:
        """
        Lock Party

        :param db: Database Session
        :param db_obj: Party instance
        """
        db_obj.locked = True

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDServer(CRUDBase[models.Server, models.ServerCreate, models.ServerUpdate]):
    def get_by_discord_id(self, db: Session, *, discord_id: str) -> models.Server:
        return (
            db.query(self.model).filter(models.Server.discord_id == discord_id).first()
        )


class CRUDChannel(CRUDBase[models.Channel, models.ChannelCreate, models.ChannelUpdate]):
    def get_multi_by_server(
        self, db: Session, *, server_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Channel]:
        # return (
        #     db.query(self.model)
        #     .filter(channels.Channel.server_id == server_id)
        #     .offset(skip)
        #     .limit(limit)
        #     .all()
        # )
        return db.exec(
            select(self.model)
            .filter(models.Channel.server_id == server_id)
            .offset(skip)
            .limit(limit)
        ).all()

    def get_multi_by_servers(
        self, db: Session, *, server_ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[models.Channel]:
        # return (
        #     db.query(self.model)
        #     .filter(col(channels.Channel.server_id).in_(server_ids))
        #     .offset(skip)
        #     .limit(limit)
        #     .all()
        # )
        return db.exec(
            select(self.model)
            .filter(col(models.Channel.server_id).in_(server_ids))
            .offset(skip)
            .limit(limit)
        ).all()


class CRUDPlayer(CRUDBase[models.Player, models.PlayerCreate, models.PlayerUpdate]):
    pass


class CRUDMember(CRUDBase[models.Member, models.MemberCreate, models.MemberUpdate]):
    def get_multi_by_party(
        self, db: Session, *, party_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Member]:
        # return (
        #     db.query(self.model)
        #     .filter(members.Member.party_id == party_id)
        #     .offset(skip)
        #     .limit(limit)
        #     .all()
        # )
        return db.exec(
            select(self.model)
            .filter(models.Member.party_id == party_id)
            .offset(skip)
            .limit(limit)
        ).all()


class CRUDRole(CRUDBase[models.Role, models.RoleCreate, models.RoleUpdate]):
    pass


class CRUDGame(CRUDBase[models.Game, models.GameCreate, models.GameUpdate]):
    pass


party = CRUDParty(models.Party)
server = CRUDServer(models.Server)
channel = CRUDChannel(models.Channel)
player = CRUDPlayer(models.Player)
member = CRUDMember(models.Member)
role = CRUDRole(models.Role)
game = CRUDGame(models.Game)
