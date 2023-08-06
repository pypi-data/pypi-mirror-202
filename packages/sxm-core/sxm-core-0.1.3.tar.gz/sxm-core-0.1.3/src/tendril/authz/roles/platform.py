

from .sxm import StarXMediaRolesTemplate


class PlatformRoleSpec(StarXMediaRolesTemplate):
    prefix = "platform"
    allowed_children = ['*']
    parent_required = False

    roles = ['Administrator',
             'Advertising Manager',
             'Media Manager',
             'Device Manager',
             'Member']
