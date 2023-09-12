from crawler import session_scope
from crawler.common.enums import NegativeKeywordMatchType, State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpCampaignNegativeKeyword


async def crawl_camp_neg_keywords(client: SponsoredProductsClient, profile_id: int) -> None:
    camp_neg_keywords = await client.get_camp_neg_keywords(profile_id)
    with session_scope() as session:
        for camp_neg_keyword in camp_neg_keywords:
            sp_campaign = session.query(SpCampaign).get(camp_neg_keyword['campaignId'])
            if sp_campaign is None:
                continue
            sp_camp_neg_keyword = session.query(SpCampaignNegativeKeyword).get(camp_neg_keyword['keywordId'])
            if sp_camp_neg_keyword is None:
                session.add(SpCampaignNegativeKeyword(
                    id=camp_neg_keyword['keywordId'],
                    keyword_text=camp_neg_keyword['keywordText'],
                    match_type=NegativeKeywordMatchType(camp_neg_keyword['matchType']),
                    state=State(camp_neg_keyword['state']),
                    campaign_id=sp_campaign.id
                ))
