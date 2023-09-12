from enum import Enum


class AccountType(Enum):
    VENDOR = 'vendor'
    SELLER = 'seller'
    AGENCY = 'agency'


class BudgetType(Enum):
    LIFETIME = 'lifetime'
    DAILY = 'daily'


class State(Enum):
    PAUSED = 'paused'
    ENABLED = 'enabled'
    ARCHIVED = 'archived'


class KeywordState(Enum):
    PAUSED = 'paused'
    ENABLED = 'enabled'
    ARCHIVED = 'archived'
    PENDING = 'pending'
    DRAFT = 'draft'


class KeywordMatchType(Enum):
    EXACT = 'exact'
    PHRASE = 'phrase'
    BROAD = 'broad'


class NegativeKeywordMatchType(Enum):
    NEGATIVE_EXACT = 'negativeExact'
    NEGATIVE_PHRASE = 'negativePhrase'


class ExpressionType(Enum):
    MANUAL = 'manual'
    AUTO = 'auto'


class RecordType(Enum):
    KEYWORDS = 'keywords'
    PRODUCT_ADS = 'productAds'
    ASINS = 'asins'
    TARGETS = 'targets'


class ApiBaseUrl(Enum):
    NORTH_AMERICA = 'https://advertising-api.amazon.com'  # North America (NA). Covers US, CA, MX, and BR marketplaces
    EUROPE = 'https://advertising-api-eu.amazon.com'  # Europe (EU). Covers UK, FR, IT, ES, DE, NL, and AE marketplaces
    FAR_EAST = 'https://advertising-api-fe.amazon.com'  # Far East (FE). Covers JP and AU marketplaces.
    SANDBOX_TEST = 'https://advertising-api-test.amazon.com'  # Sandbox Environment. Covers all marketplaces


class Region(Enum):
    NA = 'North America'
    EU = 'Europe'
    FE = 'Far East'


class CountryCode(Enum):
    US = 'United States'
    CA = 'Canada'
    MX = 'Mexico'
    BR = 'Brazil'
    UK = 'United Kingdom'
    DE = 'Germany'
    FR = 'France'
    ES = 'Spain'
    IT = 'Italy'
    NL = 'The Netherlands'
    AE = 'United Arab Emirates'
    JP = 'Japan'
    AU = 'Australia'


class CampaignType(Enum):
    SP = 'sp'
    SB = 'sb'
    SD = 'sd'
