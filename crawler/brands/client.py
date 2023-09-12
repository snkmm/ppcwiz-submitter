from typing import List

from crawler.common.enums import ApiBaseUrl
from crawler.common.networks import RestClient

KEYWORDS_METRICS = 'campaignId,' \
                   'campaignName,' \
                   'adGroupId,' \
                   'adGroupName,' \
                   'campaignStatus,' \
                   'campaignBudget,' \
                   'keywordText,' \
                   'keywordStatus,' \
                   'impressions,' \
                   'clicks,' \
                   'cost,' \
                   'attributedSales14d,' \
                   'attributedConversions14d'


TARGETS_METRICS = 'campaignId,' \
                  'campaignName,' \
                  'adGroupId,' \
                  'adGroupName,' \
                  'targetingExpression,' \
                  'targetingText,' \
                  'impressions,' \
                  'clicks,' \
                  'cost,' \
                  'attributedSales14d,' \
                  'attributedConversions14d'


class SponsoredBrandsClient(RestClient):
    def __init__(self, loop, token_type, access_token):
        super().__init__(loop, token_type, access_token)

    async def get_campaigns(self, profile_id) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/campaigns',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_ad_groups(self, profile_id) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/adGroups',
            params={},
            profile_id=profile_id
        )

    async def get_keywords(self, profile_id) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/keywords',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_neg_keywords(self, profile_id) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/negativeKeywords',
            params={'stateFilter': 'enabled'},
            profile_id=profile_id
        )

    async def create_keywords(self, profile_id: int, keywords: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/keywords',
            body=keywords,
            profile_id=profile_id
        )

    async def create_neg_keywords(self, profile_id: int, neg_keywords: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/sb/negativeKeywords',
            body=neg_keywords,
            profile_id=profile_id
        )

    async def generate_report(self, profile_id: int, record_type: str, report_date: str):
        if record_type == 'keywords':
            body = {
                'segment': 'query',
                'reportDate': report_date,
                'metrics': KEYWORDS_METRICS,
            }
        else:
            body = {
                'reportDate': report_date,
                'metrics': TARGETS_METRICS,
            }
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(body)
        return await self.post_report(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/hsa/{record_type}/report',
            body=body,
            profile_id=profile_id
        )

    async def generate_report_creative(self, profile_id: int, record_type: str, report_date: str, creative_type=None):
        if record_type == 'keywords':
            body = {
                'segment': 'query',
                'reportDate': report_date,
                'metrics': KEYWORDS_METRICS,
                'creativeType': 'video'
            }
        else:
            body = {
                'reportDate': report_date,
                'metrics': TARGETS_METRICS,
                'creativeType': 'video'
            }
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(body)
        return await self.post_report(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/hsa/{record_type}/report',
            body=body,
            profile_id=profile_id
        )
