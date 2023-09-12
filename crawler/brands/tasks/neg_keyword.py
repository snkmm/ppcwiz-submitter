from crawler import session_scope
from crawler.brands.client import SponsoredBrandsClient
from crawler.common.enums import KeywordState, NegativeKeywordMatchType
from crawler.brands.models import SbCampaign, SbNegativeKeyword


async def crawl_neg_keywords(client: SponsoredBrandsClient, profile_id: int) -> None:
    neg_keywords = await client.get_neg_keywords(profile_id)
    with session_scope() as session:
        for neg_keyword in neg_keywords:
            sb_campaign = session.query(SbCampaign).get(neg_keyword['campaignId'])
            if sb_campaign is None:
                continue
            sb_neg_keyword = session.query(SbNegativeKeyword).get(neg_keyword['keywordId'])
            if sb_neg_keyword is None:
                session.add(SbNegativeKeyword(
                    id=neg_keyword['keywordId'],
                    state=KeywordState(neg_keyword['state']),
                    keyword_text=neg_keyword['keywordText'],
                    match_type=NegativeKeywordMatchType(neg_keyword['matchType']),
                    campaign_id=neg_keyword['campaignId'],
                    ad_group_id=neg_keyword['adGroupId']
                ))
