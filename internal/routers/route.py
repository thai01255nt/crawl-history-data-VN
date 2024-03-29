from internal.app import api

from internal.db.mongo import db

from internal.src.http.handlers.history_vn.ticket import TicketUpdateNewestController
from internal.src.http.handlers.history_vn.history_resolution_1 import HistoryResolution1UpdateNewestController
from internal.src.http.handlers.history_vn.history_resolution_d import HistoryResolutionDUpdateNewestController

api.add_resource(TicketUpdateNewestController, '/tickets/update-newest')
api.add_resource(HistoryResolution1UpdateNewestController, '/histories-resolution-1/update-newest')
api.add_resource(HistoryResolutionDUpdateNewestController, '/histories-resolution-d/update-newest')

db.create_all()
db.session.commit()
