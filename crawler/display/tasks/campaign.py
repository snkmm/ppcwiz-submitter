from loguru import logger

from crawler import session_scope
from crawler.common.enums import BudgetType, State
from crawler.display.client import SponsoredDisplayClient
from crawler.display.enums import TacticType
from crawler.display.models import SdCampaign


async def crawl_campaigns(client: SponsoredDisplayClient, profile_id: int) -> None:
    campaigns = await client.get_campaigns(profile_id)
    with session_scope() as session:
        for campaign in campaigns:
            sd_campaign = session.query(SdCampaign).get(campaign['campaignId'])
            if sd_campaign is None:
                logger.info(campaign)
                session.add(SdCampaign(
                    id=campaign['campaignId'],
                    name=campaign['name'],
                    tactic=TacticType(campaign['tactic']),
                    budget_type=BudgetType(campaign['budgetType']),
                    budget=campaign['budget'],
                    start_date=campaign['startDate'],
                    end_date=campaign.get('endDate', None),
                    state=State(campaign['state']),
                    profile_id=profile_id,
                ))
