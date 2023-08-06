

from .sxm import StarXMediaRolesTemplate
from tendril.authz.roles.artefacts import ArtefactSpec


class AdvertisingAgencyRoleSpec(StarXMediaRolesTemplate):
    prefix = 'advertising_agency'
    allowed_children = ['advertising_agency', 'advertiser']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member']


class AdvertiserRoleSpec(StarXMediaRolesTemplate):
    prefix = 'advertiser'
    allowed_children = ['advertiser', 'campaign', 'advertisement']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member']


class CampaignRoleSpec(StarXMediaRolesTemplate):
    prefix = 'campaign'
    allowed_children = ['campaign', 'advertisement']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member']


class AdvertisementRoleSpec(StarXMediaRolesTemplate):
    prefix = 'advertisement'
    allowed_children = []
    recognized_artefacts = [
        ArtefactSpec('advertisement_media', 'stored_file', 'Media Manager')
    ]
    roles = ['Administrator', 'Media Manager', 'Member']
