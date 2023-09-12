from crawler import session_scope
from crawler.brands.client import SponsoredBrandsClient
from crawler.brands.models import SbAdGroup, SbCampaign


async def crawl_ad_groups(client: SponsoredBrandsClient, profile_id: int) -> None:
    ad_groups = await client.get_ad_groups(profile_id)
    with session_scope() as session:
        for ad_group in ad_groups:
            sb_campaign = session.query(SbCampaign).get(ad_group['campaignId'])
            if sb_campaign is None:
                continue
            sb_ad_group = session.query(SbAdGroup).get(ad_group['adGroupId'])
            if sb_ad_group is None:
                session.add(SbAdGroup(
                    id=ad_group['adGroupId'],
                    name=ad_group['name'],
                    campaign_id=sb_campaign.id
                ))
