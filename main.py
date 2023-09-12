import asyncio
from datetime import date, timedelta

import uvicorn
import uvloop
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from pytz import timezone
from loguru import logger

from crawler import session_scope
from crawler.common.enums import CampaignType
from crawler.common.factory import CampaignTypeClient
from crawler.common.models import Profile, User
from crawler.common.tasks.profile import crawl_profiles

from crawler.brands.views import router as sb_router
from crawler.display.views import router as sd_router
from crawler.products.views import router as sp_router

from crawler.products.views import create_neg_keywords as sp_create_neg_keywords
from crawler.products.views import create_acoss as sp_create_acoss
from crawler.products.views import create_asins as sp_create_asins

from crawler.brands.views import create_neg_keywords as sb_create_neg_keywords
from crawler.brands.views import create_acoss as sb_create_acoss
from crawler.brands.views import create_asins as sb_create_asins

from crawler.display.views import create_acoss as sd_create_acoss

app = FastAPI()
app.include_router(sd_router, prefix='/api/v1')
app.include_router(sb_router, prefix='/api/v1')
app.include_router(sp_router, prefix='/api/v1')


@app.on_event('startup')
async def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    # await start_up_event()
    scheduler = AsyncIOScheduler()

    # submitter: sp
    scheduler.add_job(
        sp_create_neg_keywords,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )
    scheduler.add_job(
        sp_create_acoss,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )
    scheduler.add_job(
        sp_create_asins,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )

    # submitter: sb
    scheduler.add_job(
        sb_create_neg_keywords,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )
    scheduler.add_job(
        sb_create_acoss,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )
    scheduler.add_job(
        sb_create_asins,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )

    # submitter: sd
    scheduler.add_job(
        sd_create_acoss,
        'interval',
        days=1,
        start_date='2021-01-01 08:00:00',
        timezone=timezone('Asia/Seoul'),
        jitter=120
    )

    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
