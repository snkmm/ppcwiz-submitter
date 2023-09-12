from crawler import session_scope
from crawler.common.enums import ExpressionType, State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup, SpTarget


async def crawl_targets(client: SponsoredProductsClient, profile_id: int) -> None:
    targets = await client.get_targets(profile_id)
    with session_scope() as session:
        for target in targets:
            sp_campaign = session.query(SpCampaign).get(target['campaignId'])
            if sp_campaign is None:
                continue
            sp_ad_group = session.query(SpAdGroup).get(target['adGroupId'])
            if sp_ad_group is None:
                continue
            sp_target = session.query(SpTarget).get(target['targetId'])
            if sp_target is None:
                session.add(SpTarget(
                    id=target['targetId'],
                    expression_type=ExpressionType(target['expressionType']),
                    expression=target['expression'][0].get('value', None)
                    if target['expression'][0]['type'] == 'asinSameAs' else None,
                    bid=target.get('bid', None),
                    state=State(target['state']),
                    campaign_id=sp_campaign.id,
                    ad_group_id=sp_ad_group.id
                ))
