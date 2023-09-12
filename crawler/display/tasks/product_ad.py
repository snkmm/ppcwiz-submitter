from crawler import session_scope
from crawler.common.enums import State
from crawler.display.client import SponsoredDisplayClient
from crawler.display.models import SdCampaign, SdAdGroup, SdProductAd


async def crawl_product_ads(client: SponsoredDisplayClient, profile_id: int) -> None:
    product_ads = await client.get_product_ads(profile_id)
    with session_scope() as session:
        for product_ad in product_ads:
            sd_campaign = session.query(SdCampaign).get(product_ad['campaignId'])
            if sd_campaign is None:
                continue
            sd_ad_group = session.query(SdAdGroup).get(product_ad['adGroupId'])
            if sd_ad_group is None:
                continue
            sd_product_ad = session.query(SdProductAd).get(product_ad['adId'])
            if sd_product_ad is None:
                session.add(SdProductAd(
                    id=product_ad['adId'],
                    asin=product_ad['asin'],
                    sku=product_ad['sku'],
                    state=State(product_ad['state']),
                    campaign_id=sd_campaign.id,
                    ad_group_id=sd_ad_group.id
                ))
