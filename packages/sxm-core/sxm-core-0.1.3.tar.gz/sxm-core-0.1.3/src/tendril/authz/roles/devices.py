

from .sxm import StarXMediaRolesTemplate


class FleetAgencyRoleSpec(StarXMediaRolesTemplate):
    prefix = 'fleet_agency'
    allowed_children = ['fleet_agency', 'fleet']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member']


class FleetRoleSpec(StarXMediaRolesTemplate):
    prefix = 'fleet'
    allowed_children = ['fleet', 'device', 'device_content']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member']
    child_add_roles = {'device': 'Device Manager',
                       'device_content': 'Media Manager'}


class DeviceRoleSpec(StarXMediaRolesTemplate):
    prefix = 'device'
    allowed_children = ['device_content']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member']
    edit_role = 'Device Manager'
    child_add_roles = {'device_content': 'Media Manager'}

    def _custom_actions(self):
        return {
            'read_settings': ('Member', f'{self.prefix}:read'),
            'write_settings': ('Device Manager', f'{self.prefix}:write')
        }


class DeviceContentRoleSpec(StarXMediaRolesTemplate):
    prefix = 'device_content'
    allowed_children = ['device_content']
    roles = ['Administrator', 'Media Manager', 'Member']
    edit_role = 'Media Manager'
    child_add_roles = {'device_content': 'Media Manager'}
