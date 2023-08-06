

# AdvertisingAgency represents various Advertisers
# Advertisers create specific Advertisements
# Advertisers run various advertising Campaigns
# Campaigns consist of AdvertisingEvents
#   across various Devices
#   using specific Advertisements
# Advertising Agencies, Advertisers, and Campaigns can all
#   be composite entities, represent more than one of the same type

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from tendril.db.models.interests import InterestModel

from tendril.authz.roles.advertising import AdvertisingAgencyRoleSpec
from tendril.authz.roles.advertising import AdvertiserRoleSpec
from tendril.authz.roles.advertising import CampaignRoleSpec
from tendril.authz.roles.advertising import AdvertisementRoleSpec

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class AdvertisingAgencyModel(InterestModel):
    type_name = "advertising_agency"
    role_spec = AdvertisingAgencyRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class AdvertiserModel(InterestModel):
    type_name = "advertiser"
    role_spec = AdvertiserRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class CampaignModel(InterestModel):
    type_name = "campaign"
    role_spec = CampaignRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class AdvertisementModel(InterestModel):
    type_name = "advertisement"
    role_spec = AdvertisementRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }
