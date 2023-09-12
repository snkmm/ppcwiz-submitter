from os.path import join, dirname
from typing import List

import aiofiles

from crawler.common.enums import ApiBaseUrl
from crawler.common.networks import RestClient

TARGETS_METRICS = 'campaignId,' \
                  'campaignName,' \
                  'adGroupId,' \
                  'adGroupName,' \
                  'targetId,' \
                  'targetingExpression,' \
                  'targetingText,' \
                  'impressions,' \
                  'clicks,' \
                  'cost,' \
                  'attributedSales30d,' \
                  'attributedUnitsOrdered30d'


PRODUCT_ADS_METRICS = 'campaignId,' \
                      'campaignName,' \
                      'adGroupId,' \
                      'adGroupName,' \
                      'asin,' \
                      'sku'


class SponsoredDisplayClient(RestClient):
    def __init__(self, loop, access_token, token_type):
        super().__init__(loop, access_token, token_type)

    async def get_campaigns(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/campaigns',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_ad_groups(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/adGroups',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_product_ads(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/productAds',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_targets(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/targets',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    async def get_neg_targets(self, profile_id: int) -> dict:
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/negativeTargets',
            params={'stateFilter': 'enabled,paused'},
            profile_id=profile_id
        )

    #newly created
    async def create_neg_targets(self, profile_id: int, neg_targets: List[dict]) -> dict:
        return await self.post(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/negativeTargets',
            body=neg_targets,
            profile_id=profile_id
        )

    async def generate_report(self, profile_id: int, record_type: str, report_date: str):
        if record_type == 'targets':
            body = {
                'tactic': 'T00020',
                'reportDate': report_date,
                'metrics': TARGETS_METRICS
            }
        else:
            body = {
                'tactic': 'T00020',
                'reportDate': report_date,
                'metrics': PRODUCT_ADS_METRICS
            }
        return await self.post_report(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/sd/{record_type}/report',
            body=body,
            profile_id=profile_id
        )
