from crawler import session_scope
from crawler.common.enums import State
from crawler.products.client import SponsoredProductsClient
from crawler.products.enums import TargetingType
from crawler.products.models import SpCampaign


async def crawl_campaigns(client: SponsoredProductsClient, profile_id: int) -> None:
    campaigns = await client.get_campaigns(profile_id)
    with session_scope() as session:
        for campaign in campaigns:
            sp_campaign = session.query(SpCampaign).get(campaign['campaignId'])
            if sp_campaign is None:
                session.add(SpCampaign(
                    id=campaign['campaignId'],
                    name=campaign['name'],
                    targeting_type=TargetingType(campaign['targetingType']),
                    dailyBudget=campaign['dailyBudget'],
                    start_date=campaign['startDate'],
                    end_date=campaign.get('endDate', None),
                    state=State(campaign['state']),
                    profile_id=profile_id
                ))
