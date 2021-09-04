from sqlmodel import SQLModel


class GenericHTTPStatus(SQLModel):
    detail: str


get_multi_responses = {
    400: {"description": "Order parsing failed. Invalid attributes present."}
}

generic_responses = {
    401: {"model": GenericHTTPStatus},
    400: {"model": GenericHTTPStatus},
    404: {"model": GenericHTTPStatus},
}
