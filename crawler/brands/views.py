import asyncio

from fastapi import APIRouter
from loguru import logger

from crawler import session_scope
from crawler.common.enums import CampaignType
from crawler.common.factory import CampaignTypeClient
from crawler.common.models import User
from crawler.brands.models import SbFilterNegativeKeyword, SbFilterAcos, SbFilterAsin

router = APIRouter()


@router.post('/brands/negativeKeywords')
async def create_neg_keywords():
    loop = asyncio.get_running_loop()
    #sb_client = await CampaignTypeClient.create(loop, CampaignType.SB)
    with session_scope() as session:
        users = session.query(User).filter_by(keyword_active=True)
        for user in users:
            #new line
            sb_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SB)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SbFilterNegativeKeyword).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sb_filter_neg_keywords = sess_filter.all()
                ###############################################################
                logger.info(sb_filter_neg_keywords)
                if not sb_filter_neg_keywords:
                    continue
                new_neg_keywords = []

                for neg_keyword in sb_filter_neg_keywords:
                    new_neg_keywords.append({
                        'campaignId': neg_keyword.campaign_id,
                        'adGroupId': neg_keyword.ad_group_id,
                        'keywordText': neg_keyword.keyword_text,
                        'matchType': neg_keyword.match_type.value,
                    })

                response = await sb_client.create_neg_keywords(
                    profile.id,
                    new_neg_keywords
                )
                print(response)
                #if response.status == 200:
                #sb_filter_neg_keywords.update({SbFilterNegativeKeyword.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SbFilterNegativeKeyword).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SbFilterNegativeKeyword).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'


@router.post('/brands/acoss')
async def create_acoss():
    loop = asyncio.get_running_loop()
    #sb_client = await CampaignTypeClient.create(loop, CampaignType.SB)
    with session_scope() as session:
        users = session.query(User).filter_by(acos_active=True)
        for user in users:
            #new line
            sb_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SB)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SbFilterAcos).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sb_filter_neg_keywords = sess_filter.all()
                ###############################################################
                if not sb_filter_neg_keywords:
                    continue
                new_neg_keywords = []

                for neg_keyword in sb_filter_neg_keywords:
                    new_neg_keywords.append({
                        'campaignId': neg_keyword.campaign_id,
                        'adGroupId': neg_keyword.ad_group_id,
                        'keywordText': neg_keyword.keyword_text,
                        'matchType': neg_keyword.match_type.value,
                    })

                response = await sb_client.create_neg_keywords(
                    profile.id,
                    new_neg_keywords
                )
                print(response)
                #if response.status == 200:
                #sb_filter_neg_keywords.update({SbFilterAcos.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SbFilterAcos).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SbFilterAcos).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'


@router.post('/brands/asins')
async def create_asins():
    loop = asyncio.get_running_loop()
    #sb_client = await CampaignTypeClient.create(loop, CampaignType.SB)
    with session_scope() as session:
        users = session.query(User).filter_by(asin_active=True)
        for user in users:
            #new line
            sb_client = await CampaignTypeClient.create(user.refresh_token, loop, CampaignType.SB)
            for profile in user.profiles:
                ###############################################################
                sess_filter = session.query(SbFilterAsin).filter_by(
                    profile_id=profile.id,
                    active=True
                )
                sb_filter_neg_keywords = sess_filter.all()
                ###############################################################
                if not sb_filter_neg_keywords:
                    continue
                new_neg_keywords = []

                for neg_keyword in sb_filter_neg_keywords:
                    new_neg_keywords.append({
                        'adGroupId': neg_target.ad_group_id,
                        'campaignId': neg_target.campaign_id,
                        'expression': [{
                            'type': 'asinSameAs',
                            'value': neg_target.expression
                        }]
                    })

                response = await sb_client.create_neg_keywords(
                    profile.id,
                    new_neg_keywords
                )
                print(response)
                #if response.status == 200:
                #sb_filter_neg_keywords.update({SbFilterAcos.active: False})
                if (type(response) is dict):
                    if (response['code'] == 'SUCCESS'):
                        ###############################################################
                        #session.query(SbFilterAcos).update({'active': False})
                        sess_filter.update({'active': False})
                        ###############################################################
                else:
                    for res in response:
                        if (res['code'] == 'SUCCESS'):
                            ###############################################################
                            #session.query(SbFilterAcos).update({'active': False})
                            sess_filter.update({'active': False})
                            ###############################################################
    return 'Successfully created'
