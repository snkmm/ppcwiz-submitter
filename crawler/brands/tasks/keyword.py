from crawler import session_scope
from crawler.brands.client import SponsoredBrandsClient
from crawler.common.enums import KeywordState, KeywordMatchType
from crawler.brands.models import SbCampaign, SbKeyword


async def crawl_keywords(client: SponsoredBrandsClient, profile_id: int) -> None:
    keywords = await client.get_keywords(profile_id)
    with session_scope() as session:
        for keyword in keywords:
            sb_campaign = session.query(SbCampaign).get(keyword['campaignId'])
            if sb_campaign is None:
                continue
            sb_keyword = session.query(SbKeyword).get(keyword['keywordId'])
            if sb_keyword is None:
                session.add(SbKeyword(
                    id=keyword['keywordId'],
                    state=KeywordState(keyword['state']),
                    keyword_text=keyword['keywordText'],
                    match_type=KeywordMatchType(keyword['matchType']),
                    bid=keyword['bid'],
                    campaign_id=keyword['campaignId'],
                    ad_group_id=keyword['adGroupId']
                ))
