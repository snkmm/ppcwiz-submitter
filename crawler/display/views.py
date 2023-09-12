import asyncio

from fastapi import APIRouter
from loguru import logger

from crawler import session_scope
from crawler.display.models import SdFilterAcos, SdFilterAsin
from crawler.common.enums import CampaignType
from crawler.common.factory import CampaignTypeClient
from crawler.common.models import User

router = APIRouter()


@router.post('/display/acoss')
async def create_acoss():
    loop = asyncio.get_running_loop()
    #sd_client = await CampaignTypeClient.create(loop, CampaignType.SD)
    with session_scope() as session:
        users = session.query(User).filter_by(acos_active=True)
        for user in users:
            #new line
            sd_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SD)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SdFilterAsin).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sp_filter_neg_targets = sess_filter.all()
                ###############################################################
                logger.info(sp_filter_neg_targets)
                if not sp_filter_neg_targets:
                    continue
                new_neg_targets = []

                for neg_target in sp_filter_neg_targets:
                    new_neg_targets.append({
                        'state': neg_target.state.value,
                        'adGroupId': neg_target.ad_group_id,
                        'expression': [{
                            'type': 'asinSameAs',
                            'value': neg_target.expression
                        }],
                        'expressionType': neg_target.expression_type.value
                    })

                response = await sd_client.create_neg_targets(
                    profile_id=profile.id,
                    neg_targets=new_neg_targets
                )
                print(response)
                #if response.status == 200:
                #sp_filter_neg_targets.update({SdFilterAcos.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SdFilterAcos).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SdFilterAcos).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'
