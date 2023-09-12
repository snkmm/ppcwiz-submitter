import asyncio
import gzip
import os
from datetime import date, timedelta
from os.path import join, dirname

import ujson
from loguru import logger

from crawler import session_scope
from crawler.products.client import SponsoredProductsClient
from crawler.products.models import SpTargetReport


async def crawl_target_report(client: SponsoredProductsClient, profile_id: int, report_date: str) -> None:
    with session_scope() as session:
        response = await client.generate_report(profile_id, 'targets', report_date)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(response)
        success = False
        while not success:
            await asyncio.sleep(30)
            response = await client.get_report(profile_id, response['reportId'])
            try:
                if response['status'] == 'SUCCESS':
                    success = True
                    logger.info(os.getcwd())

                    file = join(dirname(os.getcwd()),f'app/reports/sponsored_products/targets_report_{profile_id}_{report_date}.json.gz')
                    await client.download(profile_id, response['location'], file)
                    with gzip.GzipFile(file, 'r') as f:
                        data = f.read()
                        report = ujson.loads(data.decode())
                    print("##############################################################")
                    date_temp = report_date[:4] + "-" + report_date[4:6] + "-" + report_date[6:]
                    for target in report:
                        session.add(SpTargetReport(
                            date=date_temp,#(date.today() - timedelta(days=3)),
                            campaign_name=target['campaignName'],
                            campaign_id=target['campaignId'],
                            ad_group_name=target['adGroupName'],
                            ad_group_id=target['adGroupId'],
                            targeting_expression=target['targetingExpression'],
                            targeting_text=target['targetingText'],
                            query=target['query'],
                            impressions=target['impressions'],
                            clicks=target['clicks'],
                            cost=target['cost'],
                            attributed_sales_7d=target['attributedSales7d'],
                            attributed_units_ordered_7d=target['attributedUnitsOrdered7d'],
                            profile_id=profile_id
                        ))
                    os.remove(file)
            except:
                continue
