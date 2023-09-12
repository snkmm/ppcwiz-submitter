from sqlalchemy import Column, BigInteger, String, Enum, Numeric, Date, DateTime, func, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from crawler import Base
from crawler.common.enums import BudgetType, State, ExpressionType
from crawler.display.enums import TacticType


class SdCampaign(Base):
    __tablename__ = 'sd_campaign'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    tactic = Column(Enum(TacticType), nullable=False)
    budget_type = Column(Enum(BudgetType), nullable=False)
    budget = Column(Numeric, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))
    ad_groups = relationship('SdAdGroup', backref='campaign')
    product_ads = relationship('SdProductAd', backref='campaign')


class SdAdGroup(Base):
    __tablename__ = 'sd_ad_group'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    default_bid = Column(Numeric, nullable=False)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sd_campaign.id'))
    product_ads = relationship('SdProductAd', backref='ad_group')
    targets = relationship('SdTarget', backref='ad_group')
    neg_targets = relationship('SdNegativeTarget', backref='ad_group')


class SdProductAd(Base):
    __tablename__ = 'sd_product_ad'

    id = Column(BigInteger, primary_key=True, index=True)
    asin = Column(String(30))
    sku = Column(String(30))
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sd_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sd_ad_group.id'))


class SdTarget(Base):
    __tablename__ = 'sd_target'

    id = Column(BigInteger, primary_key=True, index=True)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    expression = Column(String(30))
    bid = Column(Numeric)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ad_group_id = Column(BigInteger, ForeignKey('sd_ad_group.id'))


class SdNegativeTarget(Base):
    __tablename__ = 'sd_neg_target'

    id = Column(BigInteger, primary_key=True, index=True)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    expression = Column(String(30))
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ad_group_id = Column(BigInteger, ForeignKey('sd_ad_group.id'))


class SdTargetReport(Base):
    __tablename__ = 'sd_target_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    target_id = Column(BigInteger, nullable=False)
    targeting_expression = Column(String(50))
    targeting_text = Column(String(50), nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Numeric, nullable=False)
    attributed_sales_30d = Column(Numeric, nullable=False)
    attributed_units_ordered_30d = Column(Integer, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SdProductAdReport(Base):
    __tablename__ = 'sd_product_ad_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    asin = Column(String(30))
    sku = Column(String(30))
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SdFilterAcos(Base):
    __tablename__ = 'sd_filter_acos'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    state = Column(Enum(State), nullable=False)
    expression = Column(String(80), nullable=False)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SdFilterAsin(Base):
    __tablename__ = 'sd_filter_asin'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    state = Column(Enum(State), nullable=False)
    expression = Column(String(80), nullable=False)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
