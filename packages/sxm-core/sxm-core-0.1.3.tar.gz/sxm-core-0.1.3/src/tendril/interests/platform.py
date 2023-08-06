

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.platform import PlatformModel


class PlatformCreateTModel(InterestBaseCreateTModel):
    type: Literal['platform']


class PlatformTModel(PlatformCreateTModel,
                     InterestBaseReadTMixin):
    ...


class Platform(InterestBase):
    model = PlatformModel
    tmodel_create = PlatformCreateTModel
    tmodel = PlatformTModel


def load(manager):
    manager.register_interest_type('Platform', Platform)
