from crawler import session_scope
from crawler.common.enums import KeywordMatchType, State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup, SpKeyword


async def crawl_keywords(client: SponsoredProductsClient, profile_id: int) -> None:
    keywords = await client.get_keywords(profile_id)
    with session_scope() as session:
        for keyword in keywords:
            sp_campaign = session.query(SpCampaign).get(keyword['campaignId'])
            if sp_campaign is None:
                continue
            sp_ad_group = session.query(SpAdGroup).get(keyword['adGroupId'])
            if sp_ad_group is None:
                continue
            sp_keyword = session.query(SpKeyword).get(keyword['keywordId'])
            if sp_keyword is None:
                session.add(SpKeyword(
                    id=keyword['keywordId'],
                    keyword_text=keyword['keywordText'],
                    match_type=KeywordMatchType(keyword['matchType']),
                    bid=keyword.get('bid', None),
                    state=State(keyword['state']),
                    campaign_id=sp_campaign.id,
                    ad_group_id=sp_ad_group.id
                ))
