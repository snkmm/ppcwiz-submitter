from crawler import session_scope
from crawler.common.enums import State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup, SpProductAd


async def crawl_product_ads(client: SponsoredProductsClient, profile_id: int) -> None:
    product_ads = await client.get_product_ads(profile_id)
    with session_scope() as session:
        for product_ad in product_ads:
            sp_campaign = session.query(SpCampaign).get(product_ad['campaignId'])
            if sp_campaign is None:
                continue
            sp_ad_group = session.query(SpAdGroup).get(product_ad['adGroupId'])
            if sp_ad_group is None:
                continue
            sp_product_ad = session.query(SpProductAd).get(product_ad['adId'])
            if sp_product_ad is None:
                session.add(SpProductAd(
                    id=product_ad['adId'],
                    asin=product_ad['asin'],
                    sku=product_ad['sku'],
                    state=State(product_ad['state']),
                    campaign_id=sp_campaign.id,
                    ad_group_id=sp_ad_group.id
                ))
