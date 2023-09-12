from crawler import session_scope
from crawler.common.enums import State
from crawler.display.client import SponsoredDisplayClient
from crawler.display.models import SdCampaign, SdAdGroup


async def crawl_ad_groups(client: SponsoredDisplayClient, profile_id: int) -> None:
    ad_groups = await client.get_ad_groups(profile_id)
    with session_scope() as session:
        for ad_group in ad_groups:
            sd_campaign = session.query(SdCampaign).get(ad_group['campaignId'])
            if sd_campaign is None:
                continue
            sd_ad_group = session.query(SdAdGroup).get(ad_group['adGroupId'])
            if sd_ad_group is None:
                session.add(SdAdGroup(
                    id=ad_group['adGroupId'],
                    name=ad_group['name'],
                    default_bid=ad_group['defaultBid'],
                    state=State(ad_group['state']),
                    campaign_id=sd_campaign.id
                ))
