from asyncio import AbstractEventLoop

from loguru import logger

from crawler.brands.client import SponsoredBrandsClient
from crawler.common.enums import CampaignType
from crawler.display.client import SponsoredDisplayClient
from crawler.products.client import SponsoredProductsClient
from crawler.util.utils import refresh_access_token


class CampaignTypeClient:
    @classmethod
    async def create(
            cls,
            ref_tok,
            loop: AbstractEventLoop,
            campaign_type: CampaignType
    ) -> [SponsoredBrandsClient, SponsoredDisplayClient, SponsoredProductsClient]:
        auth_data = await refresh_access_token(ref_tok)
        logger.info(auth_data)
        if campaign_type == CampaignType.SB:
            return SponsoredBrandsClient(
                loop,
                auth_data['token_type'],
                auth_data['access_token']
            )
        elif campaign_type == CampaignType.SD:
            return SponsoredDisplayClient(
                loop,
                auth_data['token_type'],
                auth_data['access_token']
            )
        else:
            return SponsoredProductsClient(
                loop,
                auth_data['token_type'],
                auth_data['access_token']
            )
