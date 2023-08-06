

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.devices import DeviceContentModel


class DeviceContentCreateTModel(InterestBaseCreateTModel):
    type: Literal['device_content']


class DeviceContentTModel(DeviceContentCreateTModel,
                          InterestBaseReadTMixin):
    ...


class DeviceContent(InterestBase):
    model = DeviceContentModel
    tmodel_create = DeviceContentCreateTModel
    tmodel = DeviceContentTModel


def load(manager):
    manager.register_interest_type('DeviceContent', DeviceContent)
