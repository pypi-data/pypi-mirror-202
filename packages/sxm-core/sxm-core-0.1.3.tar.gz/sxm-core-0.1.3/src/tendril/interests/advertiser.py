

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.advertising import AdvertiserModel


class AdvertiserCreateTModel(InterestBaseCreateTModel):
    type: Literal['advertiser']


class AdvertiserTModel(AdvertiserCreateTModel,
                       InterestBaseReadTMixin):
    ...


class Advertiser(InterestBase):
    model = AdvertiserModel
    tmodel_create = AdvertiserCreateTModel
    tmodel = AdvertiserTModel


def load(manager):
    manager.register_interest_type('Advertiser', Advertiser)
