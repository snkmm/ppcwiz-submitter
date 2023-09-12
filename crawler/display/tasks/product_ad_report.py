import asyncio
import gzip
import os
from datetime import date, timedelta
from os.path import join, dirname

import ujson

from crawler import session_scope
from crawler.display.client import SponsoredDisplayClient
from crawler.display.models import SdProductAdReport


async def crawl_product_ad_report(client: SponsoredDisplayClient, profile_id, report_date: str) -> None:
    with session_scope() as session:
        response = await client.generate_report(profile_id, 'productAds', report_date)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(response)
        success = False
        while not success:
            await asyncio.sleep(30)
            response = await client.get_report(profile_id, response['reportId'])
            try:
                if response['status'] == 'SUCCESS':
                    success = True

                    file = join(dirname(os.getcwd()),f'app/reports/sponsored_display/targets_report_{profile_id}_{report_date}.json.gz')
                    await client.download(profile_id, response['location'], file)
                    with gzip.GzipFile(file, 'r') as f:
                        data = f.read()
                        report = ujson.loads(data.decode())
                    print("##############################################################")
                    date_temp = report_date[:4] + "-" + report_date[4:6] + "-" + report_date[6:]
                    for product_ad in report:
                        session.add(SdProductAdReport(
                            date=date_temp,#(date.today() - timedelta(days=3)),
                            campaign_id=product_ad['campaignId'],
                            campaign_name=product_ad['campaignName'],
                            ad_group_id=product_ad['adGroupId'],
                            ad_group_name=product_ad['adGroupName'],
                            asin=product_ad['asin'],
                            profile_id=profile_id
                        ))
                    os.remove(file)
            except:
                continue
