

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.devices import FleetAgencyModel


class FleetAgencyCreateTModel(InterestBaseCreateTModel):
    type: Literal['fleet_agency']


class FleetAgencyTModel(FleetAgencyCreateTModel,
                        InterestBaseReadTMixin):
    ...


class FleetAgency(InterestBase):
    model = FleetAgencyModel
    tmodel_create = FleetAgencyCreateTModel
    tmodel = FleetAgencyTModel


def load(manager):
    manager.register_interest_type('FleetAgency', FleetAgency)
