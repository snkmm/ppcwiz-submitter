from sqlalchemy import Column, Integer, String, BigInteger, \
    Boolean, DateTime, func, Enum, ForeignKey
from sqlalchemy.orm import relationship

from crawler.common.enums import AccountType
from crawler import Base


class User(Base):
    __tablename__ = 'dtb_user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    business_name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    mobile = Column(String(20))
    country_code = Column(String(10))
    photo = Column(String(256))
    keyword_active = Column(Boolean, server_default='0', nullable=False)
    asin_active = Column(Boolean, server_default='0', nullable=False)
    acos_active = Column(Boolean, server_default='0', nullable=False)
    amazon_id = Column(String(100), unique=True, nullable=False)
    default_profile = Column(BigInteger)
    crawled_60d = Column(Boolean, server_default='0', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    auth = Column(Integer, server_default='9', nullable=False)
    refresh_token = Column(String(2048))

    profiles = relationship('Profile', backref='user')


class Profile(Base):
    __tablename__ = 'dtb_profile'

    id = Column(BigInteger, primary_key=True, index=True)
    country_code = Column(String(5))
    currency_code = Column(String(5))
    daily_budget = Column(BigInteger)
    marketplace_id = Column(String(20))
    account_id = Column(String(20))
    account_type = Column(Enum(AccountType))
    account_name = Column(String(100))
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('dtb_user.id'))
    sb_campaigns = relationship('SbCampaign', backref='profile')
    sd_campaigns = relationship('SdCampaign', backref='profile')
    sp_campaigns = relationship('SpCampaign', backref='profile')
