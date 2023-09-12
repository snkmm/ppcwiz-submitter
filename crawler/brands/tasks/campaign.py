from crawler import session_scope
from crawler.brands.client import SponsoredBrandsClient
from crawler.common.enums import BudgetType, State
from crawler.brands.enums import AdFormat
from crawler.brands.models import SbCampaign


async def crawl_campaigns(client: SponsoredBrandsClient, profile_id: int) -> None:
    campaigns = await client.get_campaigns(profile_id)
    with session_scope() as session:
        for campaign in campaigns:
            sb_campaign = session.query(SbCampaign).get(campaign.get('campaignId'))
            if sb_campaign is None:
                session.add(SbCampaign(
                    id=campaign['campaignId'],
                    name=campaign['name'],
                    ad_format=AdFormat(campaign['adFormat']),
                    budget_type=BudgetType(campaign['budgetType']),
                    budget=campaign['budget'],
                    start_date=campaign['startDate'],
                    end_date=campaign.get('endDate', None),
                    state=State(campaign['state']),
                    profile_id=profile_id
                ))
