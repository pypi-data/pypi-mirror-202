

from typing import Literal
from pydantic import Field
from tendril.caching import transit
from tendril.iotedge import profiles
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.interests import LifecycleStatus
from tendril.db.models.devices import DeviceModel
from tendril.db.models.deviceconfig import cfg_option_spec

from tendril.authz.roles.interests import require_state
from tendril.authz.roles.interests import require_permission

from tendril.utils.db import with_db
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class DeviceCreateTModel(InterestBaseCreateTModel):
    type: Literal['device']
    appname: str = Field(..., max_length=32)


class DeviceTModel(DeviceCreateTModel,
                   InterestBaseReadTMixin):
    ...


class Device(InterestBase):
    model = DeviceModel
    tmodel_create = DeviceCreateTModel
    tmodel = DeviceTModel

    additional_fields = ['appname']

    def __init__(self, *args, appname=None, **kwargs):
        self._appname = appname
        self._profile = None
        super(Device, self).__init__(*args, **kwargs)

    @property
    def appname(self):
        if self._appname:
            return self._appname
        else:
            return self._model_instance.appname

    @with_db
    def activate(self, auth_user=None, session=None):
        super(Device, self).activate(auth_user=auth_user, session=session)

        if not self.model_instance.status == LifecycleStatus.ACTIVE:
            return

        from tendril.authn.users import find_user_by_email
        from tendril.authn.users import set_user_password
        from tendril.authn.users import create_mechanized_user
        from tendril.authn.users import get_mechanized_user_email

        username = self.name
        prefix = self.appname

        # If an account exists for the user, nuke it. We're here because
        # someone changed the device state to new, we assume for re-registration.
        mu_email = get_mechanized_user_email(username, prefix)
        mu_existing = find_user_by_email(mu_email)
        if len(mu_existing):
            logger.info(f"Changing password of exiting mechanized user {mu_existing}")
            # Change password instead of creating
            password = set_user_password(mu_existing[0])
        else:
            # Create an account for the device if it does not exist
            logger.info(f"Creating new mechanized user for {username}, {prefix}")
            password = create_mechanized_user(username, prefix)
        # Publish the generated password onto redis for transmission.
        transit.write(value=password, namespace="ott:dp", key=username)

    @with_db
    @require_permission('read_settings', strip_auth=False, required=False)
    def profile(self, auth_user=None, session=None):
        if not self._profile:
            self._profile = profiles.profile(self.appname)(self._model_instance)
        return self._profile

    @with_db
    def _apply_configuration(self, spec, settings, config, session=None):
        for key, lspec in spec.items():
            if isinstance(lspec, cfg_option_spec):
                if lspec.read_only:
                    continue
                value = getattr(settings, key)
                if value is None:
                    continue
                setattr(config, lspec.accessor, value)
            elif isinstance(lspec, dict):
                lsettings = getattr(settings, key)
                if not lsettings:
                    continue
                self._apply_configuration(lspec, lsettings, config, session=None)
            else:
                raise TypeError("Unsupported Type of key {} "
                                "for Device Configuration: {}"
                                "".format(lspec, cfg_option_spec))

    @with_db
    @require_state(LifecycleStatus.ACTIVE)
    @require_permission('write_settings', strip_auth=False)
    def configure(self, settings, auth_user=None, session=None):
        # TODO Verify settings / permissions here first
        config = self.model_instance.config
        spec = config.configuration_spec()
        self._apply_configuration(spec, settings, config, session=session)


def load(manager):
    manager.register_interest_type('Device', Device)
