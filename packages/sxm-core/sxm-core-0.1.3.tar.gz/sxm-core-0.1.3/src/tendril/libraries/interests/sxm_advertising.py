
from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager

from tendril.interests.advertising_agency import AdvertisingAgency
from tendril.interests.advertiser import Advertiser
from tendril.interests.campaign import Campaign
from tendril.interests.advertisement import Advertisement


class AdvertisingAgencyLibrary(GenericInterestLibrary):
    interest_class = AdvertisingAgency


class AdvertiserLibrary(GenericInterestLibrary):
    interest_class = Advertiser


class CampaignLibrary(GenericInterestLibrary):
    interest_class = Campaign


class AdvertisementLibrary(GenericInterestLibrary):
    interest_class = Advertisement


def load(manager: InterestLibraryManager):
    manager.install_library('advertising_agencies', AdvertisingAgencyLibrary())
    manager.install_library('advertisers', AdvertiserLibrary())
    manager.install_library('campaigns', CampaignLibrary())
    manager.install_library('advertisements', AdvertisementLibrary())
