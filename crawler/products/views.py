import asyncio

from fastapi import APIRouter
from loguru import logger

from crawler import session_scope
from crawler.common.enums import CampaignType
from crawler.common.factory import CampaignTypeClient
from crawler.common.models import User
from crawler.products.models import SpFilterNegativeKeyword, SpFilterAcos, SpFilterAsin

router = APIRouter()


@router.post('/products/negativeKeywords')
async def create_neg_keywords():
    loop = asyncio.get_running_loop()
    #sp_client = await CampaignTypeClient.create(loop, CampaignType.SP)
    with session_scope() as session:
        users = session.query(User).filter_by(keyword_active=True)
        for user in users:
            #new line
            sp_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SP)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SpFilterNegativeKeyword).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sp_filter_neg_keywords = sess_filter.all()
                ###############################################################
                logger.info(sp_filter_neg_keywords)
                if not sp_filter_neg_keywords:
                    continue
                new_neg_keywords = []

                for neg_keyword in sp_filter_neg_keywords:
                    new_neg_keywords.append({
                        'campaignId': neg_keyword.campaign_id,
                        'adGroupId': neg_keyword.ad_group_id,
                        'state': neg_keyword.state.value,
                        'keywordText': neg_keyword.keyword_text,
                        'matchType': neg_keyword.match_type.value
                    })

                response = await sp_client.create_neg_keywords(
                    profile_id=profile.id,
                    neg_keywords=new_neg_keywords
                )
                print(response)
                #if response.status == 200:
                #sp_filter_neg_keywords.update({SpFilterNegativeKeyword.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SpFilterNegativeKeyword).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SpFilterNegativeKeyword).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'


@router.post('/products/acoss')
async def create_acoss():
    loop = asyncio.get_running_loop()
    #sp_client = await CampaignTypeClient.create(loop, CampaignType.SP)
    with session_scope() as session:
        users = session.query(User).filter_by(acos_active=True)
        for user in users:
            #new line
            sp_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SP)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SpFilterAcos).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sp_filter_neg_keywords = sess_filter.all()
                ###############################################################
                logger.info(sp_filter_neg_keywords)
                if not sp_filter_neg_keywords:
                    continue
                new_neg_keywords = []

                for neg_keyword in sp_filter_neg_keywords:
                    new_neg_keywords.append({
                        'campaignId': neg_keyword.campaign_id,
                        'adGroupId': neg_keyword.ad_group_id,
                        'state': neg_keyword.state.value,
                        'keywordText': neg_keyword.keyword_text,
                        'matchType': neg_keyword.match_type.value
                    })

                response = await sp_client.create_neg_keywords(
                    profile_id=profile.id,
                    neg_keywords=new_neg_keywords
                )
                print(response)
                #if response.status == 200:
                #sp_filter_neg_keywords.update({SpFilterAcos.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SpFilterAcos).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SpFilterAcos).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'


@router.post('/products/asins')
async def create_asins():
    loop = asyncio.get_running_loop()
    #sp_client = await CampaignTypeClient.create(loop, CampaignType.SP)
    with session_scope() as session:
        users = session.query(User).filter_by(asin_active=True)
        for user in users:
            #new line
            sp_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SP)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SpFilterAsin).filter_by(
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
                        'campaignId': neg_target.campaign_id,
                        'adGroupId': neg_target.ad_group_id,
                        'state': neg_target.state.value,
                        'expression': [{
                            'value': neg_target.expression,
                            'type': 'asinSameAs'
                        }],
                        'expressionType': neg_target.expression_type.value
                    })

                response = await sp_client.create_neg_targets(
                    profile_id=profile.id,
                    neg_targets=new_neg_targets
                )
                print(response)
                #if response.status == 200:
                #sp_filter_neg_targets.update({SpFilterAsin.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SpFilterAsin).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SpFilterAsin).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'
