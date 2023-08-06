

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from tendril.db.models.interests import InterestModel
from tendril.authz.roles.platform import PlatformRoleSpec

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class PlatformModel(InterestModel):
    type_name = "platform"
    role_spec = PlatformRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }
