from os.path import join, dirname
from typing import List

import aiofiles

from crawler.common.enums import ApiBaseUrl
from crawler.common.networks import RestClient

PRODUCT_ADS_METRICS = 'campaignId,' \
                      'campaignName,' \
                      'adGroupId,' \
                      'adGroupName,' \
                      'asin,' \
                      'sku'

KEYWORDS_METRICS = 'campaignId,' \
                   'campaignName,' \
                   'adGroupId,' \
                   'adGroupName,' \
                   'keywordId,' \
                   'keywordText,' \
                   'impressions,' \
                   'clicks,' \
                   'cost,' \
                   'attributedSales7d,' \
                   'attributedUnitsOrdered7d'

TARGETS_METRICS = 'campaignId,' \
                  'campaignName,' \
                  'adGroupId,' \
                  'adGroupName,' \
                  'targetingExpression,' \
                  'targetingText,' \
                  'impressions,' \
                  'clicks,' \
                  'cost,' \
                  'attributedSales7d,' \
                  'attributedUnitsOrdered7d'


class SponsoredProductsClient(RestClient):
    def __init__(self, loop, access_token, token_type):
        super().__init__(loop, access_token, token_type)

    async def get_campaigns(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/campaigns',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_ad_groups(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/adGroups',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_product_ads(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/productAds',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_keywords(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/keywords',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_neg_keywords(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/negativeKeywords',
            params={'stateFilter': 'enabled'},
            profile_id=profile_id
        )

    async def get_camp_neg_keywords(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/campaignNegativeKeywords',
            params={},
            profile_id=profile_id
        )

    async def get_targets(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/targets',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_neg_targets(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/negativeTargets',
            params={'stateFilter': 'enabled'},
            profile_id=profile_id
        )

    async def create_keywords(self, profile_id: int, keywords: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/keywords',
            body=keywords,
            profile_id=profile_id
        )

    async def create_neg_keywords(self, profile_id: int, neg_keywords: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/negativeKeywords',
            body=neg_keywords,
            profile_id=profile_id
        )

    #newly created
    async def create_neg_targets(self, profile_id: int, neg_targets: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/negativeTargets',
            body=neg_targets,
            profile_id=profile_id
        )

    async def create_camp_neg_keywords(self, profile_id: int, camp_neg_keywords: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/campaignNegativeKeywords',
            body=camp_neg_keywords,
            profile_id=profile_id
        )

    async def generate_report(self, profile_id: int, record_type: str, report_date: str):
        if record_type == 'keywords':
            body = {
                'segment': 'query',
                'reportDate': report_date,
                'metrics': KEYWORDS_METRICS
            }
        elif record_type == 'productAds':
            body = {
                'reportDate': report_date,
                'metrics': PRODUCT_ADS_METRICS
            }
        else:
            body = {
                'segment': 'query',
                'reportDate': report_date,
                'metrics': TARGETS_METRICS
            }
        return await self.post_report(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sp/{record_type}/report',
            body=body,
            profile_id=profile_id
        )
