from .base import BaseDAO
from ..schema.ticket import TickModel


class TicketDAO(BaseDAO):
    def __init__(self):
        super().__init__(TickModel)
