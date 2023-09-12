from loguru import logger

from crawler import session_scope
from crawler.common.enums import State, NegativeKeywordMatchType
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup, SpNegativeKeyword


async def crawl_neg_keywords(client: SponsoredProductsClient, profile_id: int) -> None:
    neg_keywords = await client.get_neg_keywords(profile_id)
    with session_scope() as session:
        for neg_keyword in neg_keywords:
            logger.info(neg_keyword)
            sp_campaign = session.query(SpCampaign).get(neg_keyword['campaignId'])
            if sp_campaign is None:
                continue
            sp_ad_group = session.query(SpAdGroup).get(neg_keyword['adGroupId'])
            if sp_ad_group is None:
                continue
            sp_neg_keyword = session.query(SpNegativeKeyword).get(neg_keyword['keywordId'])
            if sp_neg_keyword is None:
                session.add(SpNegativeKeyword(
                    id=neg_keyword['keywordId'],
                    keyword_text=neg_keyword['keywordText'],
                    match_type=NegativeKeywordMatchType(neg_keyword['matchType']),
                    state=State(neg_keyword['state']),
                    campaign_id=sp_campaign.id,
                    ad_group_id=sp_ad_group.id
                ))
