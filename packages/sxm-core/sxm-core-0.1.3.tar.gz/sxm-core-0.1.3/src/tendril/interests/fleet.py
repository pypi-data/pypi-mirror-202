

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.devices import FleetModel


class FleetCreateTModel(InterestBaseCreateTModel):
    type: Literal['fleet']


class FleetTModel(FleetCreateTModel,
                  InterestBaseReadTMixin):
    ...


class Fleet(InterestBase):
    model = FleetModel
    tmodel_create = FleetCreateTModel
    tmodel = FleetTModel


def load(manager):
    manager.register_interest_type('Fleet', Fleet)
