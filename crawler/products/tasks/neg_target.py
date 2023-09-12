from crawler import session_scope
from crawler.common.enums import ExpressionType, State
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpCampaign, SpAdGroup, SpNegativeTarget


async def crawl_targets(client: SponsoredProductsClient, profile_id: int) -> None:
    neg_targets = await client.get_neg_targets(profile_id)
    with session_scope() as session:
        for neg_target in neg_targets:
            sp_campaign = session.query(SpCampaign).get(neg_target['campaignId'])
            if sp_campaign is None:
                continue
            sp_ad_group = session.query(SpAdGroup).get(neg_target['adGroupId'])
            if sp_ad_group is None:
                continue
            sp_neg_target = session.query(SpNegativeTarget).get(neg_target['targetId'])
            if sp_neg_target is None:
                session.add(SpNegativeTarget(
                    id=neg_target['targetId'],
                    expression_type=ExpressionType(neg_target['expressionType']),
                    expression=neg_target['expression'][0].get('value', None)
                    if neg_target['expression'][0]['type'] == 'asinSameAs' else None,
                    state=State(neg_target['state']),
                    campaign_id=sp_campaign.id,
                    ad_group_id=sp_ad_group.id
                ))
