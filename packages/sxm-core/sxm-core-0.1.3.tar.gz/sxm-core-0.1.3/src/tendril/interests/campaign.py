

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseReadTMixin
from tendril.db.models.advertising import CampaignModel


class CampaignCreateTModel(InterestBaseCreateTModel):
    type: Literal['campaign']


class CampaignTModel(CampaignCreateTModel,
                     InterestBaseReadTMixin):
    ...


class Campaign(InterestBase):
    model = CampaignModel
    tmodel_create = CampaignCreateTModel
    tmodel = CampaignTModel


def load(manager):
    manager.register_interest_type('Campaign', Campaign)
