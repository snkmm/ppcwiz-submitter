from crawler import session_scope
from crawler.common.enums import State, ExpressionType
from crawler.display.client import SponsoredDisplayClient
from crawler.display.models import SdAdGroup, SdTarget


async def crawl_targets(client: SponsoredDisplayClient, profile_id: int) -> None:
    targets = await client.get_targets(profile_id)
    with session_scope() as session:
        for target in targets:
            sd_ad_group = session.query(SdAdGroup).get(target['adGroupId'])
            if sd_ad_group is None:
                continue
            sd_target = session.query(SdTarget).get(target['targetId'])
            if sd_target is None:
                session.add(SdTarget(
                    id=target['targetId'],
                    expression_type=ExpressionType(target['expressionType']),
                    expression=target['expression'][0].get('value', None)
                    if target['expression'][0]['type'] == 'asinSameAs' else None,
                    bid=target.get('bid', None),
                    state=State(target['state']),
                    ad_group_id=sd_ad_group.id
                ))
