from sqlalchemy import Column, Integer, Numeric, TIMESTAMP,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()
'''Фьючерсные классы'''
''' 1H '''
class CandlestickData_f(Base):
    __tablename__ = 'candles_1h_fut'

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, unique=True, nullable=False)
    open = Column(Numeric(12,5), nullable=False)
    high = Column(Numeric(12,5), nullable=False)
    low = Column(Numeric(12,5), nullable=False)
    close = Column(Numeric(12,5), nullable=False)
    volume = Column(Numeric(22, 5), nullable=False)
    quote_asset_volume = Column(Numeric(22, 5))
    number_of_trades = Column(Integer)
    taker_buy_base_asset_volume = Column(Numeric(22, 5))
    taker_buy_quote_asset_volume = Column(Numeric(22, 5))

class TechnicalIndicators_f(Base):
    __tablename__ = 'tech_ind_1h_fut'

    id = Column(Integer, primary_key=True)
    candlestick_id = Column(Integer, ForeignKey('candles_1h_fut.id'), nullable=False)
    timestamp = Column(TIMESTAMP, unique=True, nullable=False)
    openinterest = Column(Numeric(20,5))
    openinterest_value = Column(Numeric(20, 8))
    rsi = Column(Numeric(12, 5))
    ema_20 = Column(Numeric(12, 5))
    ema_50 = Column(Numeric(12, 5))
    macd = Column(Numeric(12, 5))
    macd_signal = Column(Numeric(12, 5))
    macd_hist = Column(Numeric(12, 5))
    stoch_k = Column(Numeric(12, 5))
    stoch_d = Column(Numeric(12, 5))
    roc = Column(Numeric(12, 5))
    vwap = Column(Numeric(12, 5))
    macd_21_34_1 = Column(Numeric(12, 5))
    macd_signal_21_34_1 = Column(Numeric(12, 5))
    macd_hist_21_34_1 = Column(Numeric(12, 5))
    macd_31_144_1 = Column(Numeric(12, 5))
    macd_signal_31_144_1 = Column(Numeric(12, 5))
    macd_hist_31_144_1 = Column(Numeric(12, 5))
    tsi = Column(Numeric(12, 5))
    tsi_signal = Column(Numeric(12, 5))
    rsi_o = Column(Numeric(12, 5))
    sma_20 = Column(Numeric(12, 5))
    ema_100 =Column(Numeric(12, 5))
    ema_200 = Column(Numeric(12, 5))
    wma_20 = Column(Numeric(12, 5))
    hma_20 = Column(Numeric(12, 5))
    zlma_20 = Column(Numeric(12, 5))
    tema_20 = Column(Numeric(12, 5))
    trima_20 =Column(Numeric(12, 5))
    stochrsi = Column(Numeric(12, 5))
    stochrsi_signal = Column(Numeric(12, 5))
    kama = Column(Numeric(12, 5))
    rma = Column(Numeric(12, 5))
    rsi_sma = Column(Numeric(12, 5))
    rsx = Column(Numeric(12, 5))
    mad = Column(Numeric(12, 5))
    bbands_high = Column(Numeric(12, 5))
    bbands_low = Column(Numeric(12, 5))
    dpo = Column(Numeric(12, 5))
    kst = Column(Numeric(12, 5))
    kst_signal = Column(Numeric(12, 5))
    rsi_6 = Column(Numeric(12, 5))
    ppo = Column(Numeric(12, 5))
    ppo_signal = Column(Numeric(12, 5))
    ppo_hist = Column(Numeric(12, 5))
    trend_return = Column(Numeric(12, 5))
'''Фьючерсные классы'''
''' 1м '''

class Candle1mFut(Base):
    __tablename__ = 'candles_1m_fut'

    id = Column(Integer, primary_key=True)  # Автоинкремент
    timestamp = Column(TIMESTAMP, nullable=False)
    open = Column(Numeric(12, 5), nullable=False)  # Увеличены размерности для объемов
    high = Column(Numeric(12, 5), nullable=False)
    low = Column(Numeric(12, 5), nullable=False)
    close = Column(Numeric(12, 5), nullable=False)
    volume = Column(Numeric(22, 5), nullable=False)  # Увеличены размерности для больших объемов торгов
    quote_asset_volume = Column(Numeric(22, 5))  # Увеличены размерности
    number_of_trades = Column(Integer)
    taker_buy_base_asset_volume = Column(Numeric(22, 5))
    taker_buy_quote_asset_volume = Column(Numeric(22, 5))


class TechInd1mFut(Base):
    __tablename__ = 'tech_ind_1m_fut'

    id = Column(Integer, primary_key=True)
    candlestick_id = Column(Integer, ForeignKey('candles_1m_fut.id', ondelete='CASCADE'))  # Устанавливаем внешний ключ с каскадным удалением
    timestamp = Column(TIMESTAMP, nullable=False)
    rsi = Column(Numeric(12, 5))  # Увеличены размерности для индикаторов
    ema_20 = Column(Numeric(12, 5))
    ema_50 = Column(Numeric(12, 5))
    macd = Column(Numeric(12, 5))
    macd_signal = Column(Numeric(12, 5))
    macd_hist = Column(Numeric(12, 5))
    stoch_k = Column(Numeric(12, 5))
    stoch_d = Column(Numeric(12, 5))
    roc = Column(Numeric(12, 5))
    vwap = Column(Numeric(12, 5))
    #openinterest = Column(Numeric(20, 5)) На минутках не предоставляет, только на 5
    #openinterest_value = Column(Numeric(20, 5))
    macd_21_34_1 = Column(Numeric(12, 5))
    macd_signal_21_34_1 = Column(Numeric(12, 5))
    macd_hist_21_34_1 = Column(Numeric(12, 5))
    macd_31_144_1 = Column(Numeric(12, 5))
    macd_signal_31_144_1 = Column(Numeric(12, 5))
    macd_hist_31_144_1 = Column(Numeric(12, 5))
    tsi = Column(Numeric(12, 5))
    tsi_signal = Column(Numeric(12, 5))
    rsi_o = Column(Numeric(12, 5))
    sma_20 = Column(Numeric(12, 5))
    ema_100 = Column(Numeric(12, 5))
    ema_200 = Column(Numeric(12, 5))
    wma_20 = Column(Numeric(12, 5))
    hma_20 = Column(Numeric(12, 5))
    zlma_20 = Column(Numeric(12, 5))
    tema_20 = Column(Numeric(12, 5))
    trima_20 = Column(Numeric(12, 5))
    stochrsi = Column(Numeric(12, 5))
    stochrsi_signal = Column(Numeric(12, 5))
    kama = Column(Numeric(12, 5))
    rma = Column(Numeric(12, 5))
    rsi_sma = Column(Numeric(12, 5))
    rsx = Column(Numeric(12, 5))
    mad = Column(Numeric(12, 5))
    bbands_high = Column(Numeric(12, 5))
    bbands_low = Column(Numeric(12, 5))
    dpo = Column(Numeric(12, 5))
    kst = Column(Numeric(12, 5))
    kst_signal = Column(Numeric(12, 5))
    rsi_6 = Column(Numeric(12, 5))
    ppo = Column(Numeric(12, 5))
    ppo_signal = Column(Numeric(12, 5))
    ppo_hist = Column(Numeric(12, 5))
    trend_return = Column(Numeric(12, 5))

'''СПОТ классы'''
''' 1H '''
'''Надо восстановить'''

'''СПОТ классы'''
''' 1м '''
class CandlestickData_1m(Base):
    __tablename__ = 'candlestick_1m'

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, unique=True, nullable=False)
    open = Column(Numeric(18, 8), nullable=False)
    high = Column(Numeric(18, 8), nullable=False)
    low = Column(Numeric(18, 8), nullable=False)
    close = Column(Numeric(18, 8), nullable=False)
    volume = Column(Numeric(18, 8), nullable=False)
    quote_asset_volume = Column(Numeric(18, 8))
    number_of_trades = Column(Integer)
    taker_buy_base_asset_volume = Column(Numeric(18, 8))
    taker_buy_quote_asset_volume = Column(Numeric(18, 8))

class TechnicalIndicators_1m(Base):
    __tablename__ = 'technical_ind_1m'

    id = Column(Integer, primary_key=True)
    candlestick_id = Column(Integer, ForeignKey('candlestick_1m.id'), nullable=False)
    timestamp = Column(TIMESTAMP, unique=True, nullable=False)
    rsi = Column(Numeric(18, 8))
    ema_20 = Column(Numeric(18, 8))
    ema_50 = Column(Numeric(18, 8))
    macd = Column(Numeric(18, 8))
    macd_signal = Column(Numeric(18, 8))
    macd_hist = Column(Numeric(18, 8))
    stoch_k = Column(Numeric(18, 8))
    stoch_d = Column(Numeric(18, 8))
    roc = Column(Numeric(18, 8))
    vwap = Column(Numeric(18, 8))
    macd_21_34_1 = Column(Numeric(18, 8))
    macd_signal_21_34_1 = Column(Numeric(18, 8))
    macd_hist_21_34_1 = Column(Numeric(18, 8))
    macd_31_144_1 = Column(Numeric(18, 8))
    macd_signal_31_144_1 = Column(Numeric(18, 8))
    macd_hist_31_144_1 = Column(Numeric(18, 8))
