

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.advertising import AdvertisementModel


class AdvertisementCreateTModel(InterestBaseCreateTModel):
    type: Literal['advertisement']


class AdvertisementTModel(AdvertisementCreateTModel,
                          InterestBaseReadTMixin):
    ...


class Advertisement(InterestBase):
    model = AdvertisementModel
    tmodel_create = AdvertisementCreateTModel
    tmodel = AdvertisementTModel


def load(manager):
    manager.register_interest_type('Advertisement', Advertisement)
