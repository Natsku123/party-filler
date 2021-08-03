import dateutil.parser
import json
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core.utils import camel_dict_to_snake

from pydantic import BaseModel
from core.database import Base

from core.database import models, schemas

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

FilterParseException = HTTPException(
    status_code=400, detail="Filter parsing failed. Invalid attributes present."
)

OrderParseException = HTTPException(
    status_code=400, detail="Order parsing failed. Invalid attributes present."
)


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
                    new_filters.append(attr > v)
                elif ge:
                    new_filters.append(attr >= v)
                elif lt:
                    new_filters.append(attr < v)
                elif le:
                    new_filters.append(attr <= v)
                else:
                    new_filters.append(attr == v)
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

        order[i] = asc(v) if a and not d else desc(v) if not a and d else v
    return order


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_count(self, db: Session) -> int:
        """
        Get total number of objects in database.
        :param db: Database Session to be used
        """
        return db.query(self.model).count()

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Union[Dict, str]] = None,
        order: Optional[Union[List[str], str]] = None
    ) -> List[ModelType]:

        q = db.query(self.model)

        if filters is not None:
            if isinstance(filters, str):
                filters = json.loads(filters)

            q = q.filter(*parse_filter(filters, self.model))

        if order is not None:
            if isinstance(order, str):
                order = json.loads(order)

            q = q.order_by(*parse_order(order, self.model))

        return q.offset(skip).limit(limit).all()

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


class CRUDParty(CRUDBase[models.Party, schemas.PartyCreate, schemas.PartyUpdate]):
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
            if field in update_data and field == "start_time":
                setattr(db_obj, field, dateutil.parser.parse(update_data["start_time"]))
            elif field in update_data and field == "end_time":
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


class CRUDServer(CRUDBase[models.Server, schemas.ServerCreate, schemas.ServerUpdate]):
    def get_by_discord_id(self, db: Session, *, discord_id: str) -> models.Server:
        return (
            db.query(self.model).filter(models.Server.discord_id == discord_id).first()
        )


class CRUDChannel(
    CRUDBase[models.Channel, schemas.ChannelCreate, schemas.ChannelUpdate]
):
    def get_multi_by_server(
        self, db: Session, *, server_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Channel]:
        return (
            db.query(self.model)
            .filter(models.Channel.server_id == server_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_servers(
        self, db: Session, *, server_ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[models.Channel]:
        return (
            db.query(self.model)
            .filter(models.Channel.server_id.in_(server_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )


class CRUDPlayer(CRUDBase[models.Player, schemas.PlayerCreate, schemas.PlayerUpdate]):
    pass


class CRUDMember(CRUDBase[models.Member, schemas.MemberCreate, schemas.MemberUpdate]):
    def get_multi_by_party(
        self, db: Session, *, party_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Member]:
        return (
            db.query(self.model)
            .filter(models.Member.party_id == party_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


class CRUDRole(CRUDBase[models.Role, schemas.RoleCreate, schemas.RoleUpdate]):
    pass


class CRUDGame(CRUDBase[models.Game, schemas.GameCreate, schemas.GameUpdate]):
    pass


party = CRUDParty(models.Party)
server = CRUDServer(models.Server)
channel = CRUDChannel(models.Channel)
player = CRUDPlayer(models.Player)
member = CRUDMember(models.Member)
role = CRUDRole(models.Role)
game = CRUDGame(models.Game)
