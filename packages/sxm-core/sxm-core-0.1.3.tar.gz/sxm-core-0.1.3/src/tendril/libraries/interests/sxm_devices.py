

from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager

from tendril.interests.fleet_agency import FleetAgency
from tendril.interests.fleet import Fleet
from tendril.interests.device import Device
from tendril.interests.device_content import DeviceContent


class FleetAgencyLibrary(GenericInterestLibrary):
    interest_class = FleetAgency


class FleetLibrary(GenericInterestLibrary):
    interest_class = Fleet


class DeviceLibrary(GenericInterestLibrary):
    interest_class = Device


class DeviceContentLibrary(GenericInterestLibrary):
    interest_class = DeviceContent


def load(manager: InterestLibraryManager):
    manager.install_library('fleet_agencies', FleetAgencyLibrary())
    manager.install_library('fleets', FleetLibrary())
    manager.install_library('devices', DeviceLibrary())
    manager.install_library('device_content', DeviceContentLibrary())
