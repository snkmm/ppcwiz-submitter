from loguru import logger

from crawler import session_scope
from crawler.common.enums import State, ExpressionType
from crawler.display.client import SponsoredDisplayClient
from crawler.display.models import SdAdGroup, SdNegativeTarget


async def crawl_neg_targets(client: SponsoredDisplayClient, profile_id: int) -> None:
    neg_targets = await client.get_neg_targets(profile_id)
    with session_scope() as session:
        for neg_target in neg_targets:
            logger.info(neg_targets)
            sd_ad_group = session.query(SdAdGroup).get(neg_target['adGroupId'])
            if sd_ad_group is None:
                continue
            sd_neg_target = session.query(SdNegativeTarget).get(neg_target['targetId'])
            if sd_neg_target is None:
                session.add(SdNegativeTarget(
                    id=neg_target['targetId'],
                    expression_type=ExpressionType(neg_target['expressionType']),
                    expression=neg_target['expression'][0].get('value', None)
                    if neg_target['expression'][0]['type'] == 'asinSameAs' else None,
                    state=State(neg_target['state']),
                    ad_group_id=sd_ad_group.id
                ))
