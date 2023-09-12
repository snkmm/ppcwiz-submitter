from sqlalchemy import Column, BigInteger, String, DateTime, func, Date, ForeignKey, Integer, Numeric, Enum, Boolean
from sqlalchemy.orm import relationship

from crawler import Base
from crawler.common.enums import State, KeywordMatchType, ExpressionType, NegativeKeywordMatchType
from crawler.products.enums import TargetingType


class SpCampaign(Base):
    __tablename__ = 'sp_campaign'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    targeting_type = Column(Enum(TargetingType), nullable=False)
    dailyBudget = Column(Numeric, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))
    ad_groups = relationship('SpAdGroup', backref='campaign')
    product_ads = relationship('SpProductAd', backref='campaign')
    keywords = relationship('SpKeyword', backref='campaign')
    neg_keywords = relationship('SpNegativeKeyword', backref='campaign')
    camp_neg_keywords = relationship('SpCampaignNegativeKeyword', backref='campaign')


class SpAdGroup(Base):
    __tablename__ = 'sp_ad_group'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    default_bid = Column(Numeric, nullable=False)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    product_ads = relationship('SpProductAd', backref='ad_group')
    keywords = relationship('SpKeyword', backref='ad_group')
    neg_keywords = relationship('SpNegativeKeyword', backref='ad_group')


class SpProductAd(Base):
    __tablename__ = 'sp_product_ad'

    id = Column(BigInteger, primary_key=True, index=True)
    asin = Column(String(30), nullable=False)
    sku = Column(String(30), nullable=False)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sp_ad_group.id'))


class SpKeyword(Base):
    __tablename__ = 'sp_keyword'

    id = Column(BigInteger, primary_key=True, index=True)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(KeywordMatchType), nullable=False)
    bid = Column(Numeric)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sp_ad_group.id'))


class SpNegativeKeyword(Base):
    __tablename__ = 'sp_neg_keyword'

    id = Column(BigInteger, primary_key=True, index=True)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sp_ad_group.id'))


class SpCampaignNegativeKeyword(Base):
    __tablename__ = 'sp_camp_neg_keyword'

    id = Column(BigInteger, primary_key=True, index=True)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))


class SpTarget(Base):
    __tablename__ = 'sp_target'

    id = Column(BigInteger, primary_key=True, index=True)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    expression = Column(String(30))
    bid = Column(Numeric)
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sp_ad_group.id'))


class SpNegativeTarget(Base):
    __tablename__ = 'sp_neg_target'

    id = Column(BigInteger, primary_key=True, index=True)
    expression_type = Column(Enum(ExpressionType), nullable=False)
    expression = Column(String(30))
    state = Column(Enum(State), nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    campaign_id = Column(BigInteger, ForeignKey('sp_campaign.id'))
    ad_group_id = Column(BigInteger, ForeignKey('sp_ad_group.id'))


class SpProductAdReport(Base):
    __tablename__ = 'sp_product_ad_report'

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


class SpKeywordReport(Base):
    __tablename__ = 'sp_keyword_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    keyword_id = Column(BigInteger, nullable=False)
    keyword_text = Column(String(80), nullable=False)
    query = Column(String(200), nullable=False)
    impressions = Column(BigInteger, nullable=False)
    clicks = Column(BigInteger, nullable=False)
    cost = Column(Numeric, nullable=False)
    attributed_sales_7d = Column(Numeric, nullable=False)
    attributed_units_ordered_7d = Column(Integer, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SpTargetReport(Base):
    __tablename__ = 'sp_target_report'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    campaign_name = Column(String(128), nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    ad_group_name = Column(String(255), nullable=False)
    targeting_expression = Column(String(50))
    targeting_text = Column(String(50), nullable=False)
    query = Column(String(200), nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Numeric, nullable=False)
    attributed_sales_7d = Column(Numeric, nullable=False)
    attributed_units_ordered_7d = Column(Integer, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile_id = Column(BigInteger, ForeignKey('dtb_profile.id'))


class SpFilterNegativeKeyword(Base):
    __tablename__ = 'sp_filter_neg_keyword'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    state = Column(Enum(State), nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SpFilterAcos(Base):
    __tablename__ = 'sp_filter_acos'

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(BigInteger, nullable=False)
    campaign_id = Column(BigInteger, nullable=False)
    ad_group_id = Column(BigInteger, nullable=False)
    state = Column(Enum(State), nullable=False)
    keyword_text = Column(String(80), nullable=False)
    match_type = Column(Enum(NegativeKeywordMatchType), nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SpFilterAsin(Base):
    __tablename__ = 'sp_filter_asin'

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
