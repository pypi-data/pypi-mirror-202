

from typing import Literal
from typing import Optional
from functools import lru_cache
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from tendril.utils.pydantic import TendrilTBaseModel
from tendril.db.models.deviceconfig import DeviceConfigurationModel
from tendril.db.models.deviceconfig import cfg_option_spec


class SXMDeviceConfigurationModel(DeviceConfigurationModel):
    device_type = "sxm"
    id = Column(Integer, ForeignKey(DeviceConfigurationModel.id), primary_key=True)

    allow_local_usb = Column(Boolean, nullable=False, default=False)
    portrait = Column(Boolean, nullable=False, default=False)
    flip = Column(Boolean, nullable=False, default=False)
    default_content_id = Column(Integer, ForeignKey('DeviceContent.id'))

    @declared_attr
    def default_content(cls):
        return relationship('DeviceContentModel', lazy='selectin')

    @classmethod
    @lru_cache(maxsize=None)
    def configuration_spec(cls):
        rv = super(SXMDeviceConfigurationModel, cls).configuration_spec()
        rv['display'] = {'portrait': cfg_option_spec('Portait Orientation', 'portrait', bool, default=False),
                         'flip': cfg_option_spec('Flip Display Orientation', 'flip', bool, default=False)}
        rv['local_usb'] = {'allow': cfg_option_spec('Allow local USB content', 'allow_local_usb', bool, default=False)}
        return rv

    __mapper_args__ = {
        "polymorphic_identity": device_type,
    }
