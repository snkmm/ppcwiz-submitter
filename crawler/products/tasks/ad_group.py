from crawler import session_scope
from crawler.common.enums import State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup


async def crawl_ad_groups(client: SponsoredProductsClient, profile_id: int) -> None:
    ad_groups = await client.get_ad_groups(profile_id)
    with session_scope() as session:
        for ad_group in ad_groups:
            sp_campaign = session.query(SpCampaign).get(ad_group['campaignId'])
            if sp_campaign is None:
                continue
            sd_ad_group = session.query(SpAdGroup).get(ad_group['adGroupId'])
            if sd_ad_group is None:
                session.add(SpAdGroup(
                    id=ad_group['adGroupId'],
                    name=ad_group['name'],
                    default_bid=ad_group['defaultBid'],
                    state=State(ad_group['state']),
                    campaign_id=sp_campaign.id
                ))
