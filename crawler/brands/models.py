from sqlalchemy import \
    Column, BigInteger, String, Enum, Numeric, Date, \
    DateTime, func, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from crawler.common.enums import BudgetType, State, \
    KeywordState, KeywordMatchType, NegativeKeywordMatchType, ExpressionType
from crawler import Base
from crawler.brands.enums import AdFormat


class SbCampaign(Base):
    __tablename__ = 'sb_campaign'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    ad_format = Column(Enum(AdFormat), nullable=False)
    budget_type = Column(Enum(BudgetType), nullable=False)
    budget = Column(Numeric, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))
    ad_groups = relationship('SbAdGroup', backref='campaign')
    keywords = relationship('SbKeyword', backref='campaign')
    neg_keywords = relationship('SbNegativeKeyword', backref='campaign')


class SbAdGroup(Base):
    __tablename__ = 'sb_ad_group'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sb_campaign.id'))
    keywords = relationship('SbKeyword', backref='ad_group')
    neg_keywords = relationship('SbNegativeKeyword', backref='ad_group')


class SbKeyword(Base):
    __tablename__ = 'sb_keyword'

    id = Column(BigInteger, primary_key=True, index=True)
    state = Column(Enum(KeywordState), nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(KeywordMatchType), nullable=False)
    bid = Column(Numeric)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sb_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sb_ad_group.id'))


class SbNegativeKeyword(Base):
    __tablename__ = 'sb_neg_keyword'

    id = Column(BigInteger, primary_key=True, index=True)
    state = Column(Enum(KeywordState), nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sb_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sb_ad_group.id'))


class SbKeywordReport(Base):
    __tablename__ = 'sb_keyword_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    campaign_status = Column(String(20), nullable=False)
    campaign_budget = Column(Numeric, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    keyword_text = Column(String(80), nullable=False)
    keyword_status = Column(String(20), nullable=False)
    query = Column(String(200), nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Numeric, nullable=False)
    attributed_sales_14d = Column(Numeric, nullable=False)
    attributed_conversions_14d = Column(Numeric, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SbTargetReport(Base):
    __tablename__ = 'sb_target_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    targeting_expression = Column(String(50))
    targeting_text = Column(String(50), nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Numeric, nullable=False)
    attributed_sales_14d = Column(Numeric, nullable=False)
    attributed_conversions_14d = Column(Integer, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SbFilterNegativeKeyword(Base):
    __tablename__ = 'sb_filter_neg_keyword'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SbFilterAcos(Base):
    __tablename__ = 'sb_filter_acos'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SbFilterAsin(Base):
    __tablename__ = 'sb_filter_asin'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    expression = Column(String(80), nullable=False)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
