#!pip install sqlalchemy 
import requests
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from sqlalchemy import create_engine, text
from binance.client import Client
from datetime import datetime, timedelta
from prophet import Prophet
from prophet.make_holidays import make_holidays_df
import pickle
from sqlalchemy import create_engine, text

from tqdm import tqdm

import time
pd.options.display.max_columns = None
pd.options.display.max_rows = None

import warnings
warnings.filterwarnings("ignore")

api_key = ''
api_secret = ''

PREDEFINED_PARAMS = {
     'changepoint_prior_scale': 0.4176933439369656, 
     'seasonality_prior_scale': 2.8272453308262318,
     'changepoint_range': 0.9499976369923773, 
     'yearly_fourier_order': 9, 
     'weekly_fourier_order': 10, 
     'daily_fourier_order': 9, 
     'hourly_fourier_order': 8, 
     'monthly_fourier_order': 8}

ticker = 'BTC'

client = Client(api_key, api_secret)

'''
BASE_URL = "https://api.coingecko.com/api/v3"
def get_marketcap_and_volume0(coin_id='bitcoin', vs_currency='usd', days=364):
    """
    Получает данные о рыночной капитализации и объеме торгов для заданной монеты.
    Args:
        coin_id (str): свои ID монеты для CoinGecko ( "bitcoin").
        vs_currency (str): зачем то валюта ("usd").
        days (int or str): Количество дней  максимально 365
    Returns:
        pd.DataFrame: DataFrame с колонками date, marketcap, volume.
    """
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        market_caps = data['market_caps']  # Список [timestamp, market_cap]
        volumes = data['total_volumes']  # Список [timestamp, volume]
        prices = data['prices'] 
        df = pd.DataFrame({
            "timestamp": [datetime.utcfromtimestamp(m[0] / 1000) for m in market_caps],
            "market_cap": [m[1] for m in market_caps],
            "total_volume": [v[1] for v in volumes],
            "prices": [p[1] for p in prices]
        })
        # Добавим в читабельном виде
        #df['marketcap_readble'] = df['marketcap'].apply(lambda x: f"{x:,.2f}")
        #df['volume_readble'] = df['volume'].apply(lambda x: f"{x:,.2f}")
        # Преобразуем timestamp в дату и группируем по последнему значению за день
        df['date'] = df['timestamp'].dt.date
        df = df.groupby('date').last().reset_index()
        df['snapped_at'] = df['timestamp'].apply(lambda x: int(x.timestamp() * 1000))
        df=df.drop(columns=['date'])
        return df
    else:
        raise Exception(f"Error fetching: {response.status_code}")
'''
def get_global_cap_and_volume():
    """
    Получает данные из таблицы global_cap.
    Возращает   pd.DataFrame: DataFrame с колонками date, market_cap, total_volume.
    """
   # Параметры подключения
   # from sqlalchemy import create_engine, text

    host = 'db_db_1'
    port = '5432'
    database = 'FinTech6_BTC'
    user = 'fintech_user'
    password = 'user'

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    try:
        with engine.connect() as connection:
            # Запрос для объединения таблиц по timestamp
            query = """
            SELECT *
            FROM global_cap
            ORDER BY snapped_at;
            """
            # Загружаем данные в DataFrame
            df = pd.read_sql_query(query, connection)
            # Преобразуем timestamp в дату и группируем по последнему значению за день
            df['snapped_at'] = pd.to_datetime(df['snapped_at'], unit='ms')
            # Перевод в миллисекунды
            df['snapped_at'] = df['snapped_at'].apply(lambda x: int(x.timestamp() * 1000))
            df['date'] = pd.to_datetime(df['snapped_at'], unit='ms')#datetime.utcfromtimestamp(df['snapped_at'] / 1000)#df['timestamp'].dt.date
            df = df.groupby('date').last().reset_index()
            df = df.drop(columns=['date'])
            return df
    except Exception as e:
        print("Ошибка при подключении к базе данных:", e)
    finally:
        engine.dispose()
def get_btc_cap_and_volume():
    """
    Получает данные из таблицы btc_cap.
    Возращает   pd.DataFrame: DataFrame с колонками snapped_at, market_cap, total_volume.
    """
   # Параметры подключения
   # from sqlalchemy import create_engine, text

    host = 'db_db_1'
    port = '5432'
    database = 'FinTech6_BTC'
    user = 'fintech_user'
    password = 'user'

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    try:
        with engine.connect() as connection:
            # Запрос для объединения таблиц по timestamp
            query = """
            SELECT *
            FROM btc_cap
            ORDER BY snapped_at;
            """
            df = pd.read_sql_query(query, connection)
            # Убираем "UTC" и преобразуем в datetime
            df['snapped_at'] = pd.to_datetime(df['snapped_at'].str.replace(" UTC", "", regex=False))
            # Перевод в миллисекунды
            df['snapped_at'] = df['snapped_at'].apply(lambda x: int(x.timestamp() * 1000))
            #df['date'] = pd.to_datetime(df['snapped_at'], unit='ms')#datetime.utcfromtimestamp(df['snapped_at'] / 
            return df
    except Exception as e:
        print("Ошибка при подключении к базе данных:", e)
    finally:
        engine.dispose()

def fetch_data_with_intervals(fetch_function, symbol, start_time, end_time, interval_hours=1000):
    data = []
    current_start = start_time
    total_intervals = int((end_time - start_time).total_seconds() // (interval_hours * 3600)) + 1
    print(f"Fetching data for {symbol} from {start_time} to {end_time} in {total_intervals} intervals...")
    
    for _ in tqdm(range(total_intervals), desc="Fetching data"):
        current_end = current_start + timedelta(hours=interval_hours)
        if current_end > end_time:
            current_end = end_time

        fetched_data = fetch_function(symbol, current_start, current_end)
        data.extend(fetched_data)

        current_start = current_end + timedelta(milliseconds=1)
        time.sleep(0.1)

    print(f"Completed fetching data for {symbol}. Total records: {len(data)}")
    return data

# Загрузка FGI
def fetch_fgi():
    print("Fetching Fear & Greed Index data...")
    url = 'https://api.alternative.me/fng/?limit=0&date_format=us'
    fgi_data = requests.get(url).json()['data']
    fgi_df = pd.DataFrame(fgi_data)
    fgi_df['timestamp'] = pd.to_datetime(fgi_df['timestamp'])
    fgi_df['FG'] = fgi_df['value'].astype(int)
    fgi_df = fgi_df[['timestamp', 'FG']].sort_values(by='timestamp')
    print(f"FGI data loaded. Total records: {len(fgi_df)}")
    return fgi_df

# Загрузка свечей
def fetch_candlestick_data(symbol, interval):
    print(f"Fetching candlestick data for {interval} interval from Binance...")
    start_date = '2016-01-01 00:00:00'
    klines = client.get_historical_klines(symbol, interval, start_date, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                       'close_time', 'quote_asset_volume', 'number_of_trades', 
                                       'taker_buy_base', 'taker_buy_quote', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    columns_to_convert = ['open', 'high', 'low', 'close', 'volume', 'number_of_trades', 'taker_buy_base', 'quote_asset_volume', 'taker_buy_quote']
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote']]
    print(f"Candlestick data for {interval} interval loaded. Total records: {len(df)}")
    return df

# Загрузка Funding Rate
def fetch_funding_rate(symbol, start_time, end_time):
    BASE_URL = 'https://fapi.binance.com'
    params = {
        'symbol': symbol,
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000),
        'limit': 1000
    }
    return requests.get(f"{BASE_URL}/fapi/v1/fundingRate", params=params).json()

def fetch_funding_data(symbol):
    print("Fetching Funding Rate data...")
    funding_data = fetch_data_with_intervals(fetch_funding_rate, symbol, datetime(2016, 1, 1), datetime.now())
    funding_df = pd.DataFrame(funding_data)
    funding_df['timestamp'] = pd.to_datetime(funding_df['fundingTime'], unit='ms')
    funding_df['fundingRate'] = pd.to_numeric(funding_df['fundingRate'], errors='coerce')
    funding_df.dropna(inplace=True)
    funding_df = funding_df[['timestamp', 'fundingRate']].sort_values(by='timestamp')
    print(f"Funding Rate data loaded. Total records: {len(funding_df)}")
    return funding_df

# Создание датасетов для нескольких временных фреймов
#timeframes = {
#    '1h': Client.KLINE_INTERVAL_1HOUR
    #'2h': Client.KLINE_INTERVAL_2HOUR,
    #'4h': Client.KLINE_INTERVAL_4HOUR,
    #'1d': Client.KLINE_INTERVAL_1DAY
    #}

def calculate_indicators(merged_df):
    # Убедимся, что индекс является datetime
    if not isinstance(merged_df.index, pd.DatetimeIndex):
        if 'timestamp' in merged_df.columns:
            merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'])
            merged_df.set_index('timestamp', inplace=True)
        else:
            raise ValueError("Dataset must have a 'timestamp' column with datetime values.")

    # Индикаторы на основе закрытия цены
    merged_df['rsi'] = ta.rsi(merged_df['close'], length=14)
    merged_df['ema_20'] = ta.ema(merged_df['close'], length=20)
    merged_df['ema_50'] = ta.ema(merged_df['close'], length=50)
    merged_df['ema_100'] = ta.ema(merged_df['close'], length=100)
    merged_df['ema_200'] = ta.ema(merged_df['close'], length=200)
    merged_df['sma_20'] = ta.sma(merged_df['close'], length=20)

    # MACD
    macd = ta.macd(merged_df['close'], fast=12, slow=26, signal=9)
    merged_df['macd'] = macd['MACD_12_26_9']
    merged_df['macd_signal'] = macd['MACDs_12_26_9']
    merged_df['macd_hist'] = macd['MACDh_12_26_9']

    # Stochastic RSI
    stoch_rsi = ta.stochrsi(merged_df['close'])
    merged_df['stochrsi'] = stoch_rsi['STOCHRSIk_14_14_3_3']
    merged_df['stochrsi_signal'] = stoch_rsi['STOCHRSId_14_14_3_3']

    # Stochastic
    stoch = ta.stoch(merged_df['high'], merged_df['low'], merged_df['close'])
    merged_df['stoch_k'] = stoch['STOCHk_14_3_3']
    merged_df['stoch_d'] = stoch['STOCHd_14_3_3']

    # Другие индикаторы
    merged_df['roc'] = ta.roc(merged_df['close'], length=12)
    merged_df['vwap'] = ta.vwap(merged_df['high'], merged_df['low'], merged_df['close'], merged_df['volume'])
    merged_df['kama'] = ta.kama(merged_df['close'], length=10)
    merged_df['rma'] = ta.rma(merged_df['close'], length=14)
    merged_df['hma_20'] = ta.hma(merged_df['close'], length=20)
    merged_df['zlma_20'] = ta.zlma(merged_df['close'], length=20)
    merged_df['tema_20'] = ta.tema(merged_df['close'], length=20)
    merged_df['trima_20'] = ta.trima(merged_df['close'], length=20)
    merged_df['wma_20'] = ta.wma(merged_df['close'], length=20)
    merged_df['rsx'] = ta.rsx(merged_df['close'], length=14)
    merged_df['mad'] = ta.mad(merged_df['close'], length=10)

    # Bollinger Bands
    bbands = ta.bbands(merged_df['close'], length=20)
    merged_df['bbands_high'] = bbands['BBU_20_2.0']
    merged_df['bbands_low'] = bbands['BBL_20_2.0']

    # Расчет DPO
    period = 20
    sma = merged_df['close'].rolling(window=period).mean()
    shift = int(period / 2 + 1)
    
    # Основной расчет DPO
    merged_df['dpo'] = merged_df['close'] - sma.shift(shift)

    # Заполнение DPO для последних периодов
    last_values = merged_df['close'] - sma
    merged_df['dpo'].fillna(last_values, inplace=True)

    # KST
    kst = ta.kst(merged_df['close'])
    merged_df['kst'] = kst['KST_10_15_20_30_10_10_10_15']
    merged_df['kst_signal'] = kst['KSTs_9']

    # PPO
    ppo = ta.ppo(merged_df['close'])
    merged_df['ppo'] = ppo['PPO_12_26_9']
    merged_df['ppo_signal'] = ppo['PPOs_12_26_9']
    merged_df['ppo_hist'] = ppo['PPOh_12_26_9']

    # RSI с коротким периодом
    merged_df['rsi_6'] = ta.rsi(merged_df['close'], length=6)
    merged_df['trend_return'] = ta.roc(merged_df['close'], length=6)

    # Расчёт дельты
    merged_df['buy_volume'] = merged_df['taker_buy_base']
    merged_df['sell_volume'] = merged_df['volume'] - merged_df['buy_volume']
    merged_df['delta'] = merged_df['buy_volume'] - merged_df['sell_volume']
    merged_df['cumulative_delta'] = merged_df['delta'].cumsum()

    # Индикаторы на основе OHLC
    merged_df['atr'] = ta.atr(merged_df['high'], merged_df['low'], merged_df['close'], length=14)
    adx = ta.adx(merged_df['high'], merged_df['low'], merged_df['close'], length=14)
    merged_df['adx'] = adx['ADX_14']
    merged_df['adx_pos'] = adx['DMP_14']
    merged_df['adx_neg'] = adx['DMN_14']
    merged_df['chaikin'] = ta.ad(merged_df['high'], merged_df['low'], merged_df['close'], merged_df['volume'])
    merged_df['ad'] = ta.ad(merged_df['high'], merged_df['low'], merged_df['close'], merged_df['volume'])

    # Преобразование типов для MFI
    merged_df['mfi'] = ta.mfi(
        merged_df['high'], 
        merged_df['low'], 
        merged_df['close'], 
        merged_df['volume'], 
        length=14
        ).astype(float)

    merged_df['williams_r'] = ta.willr(merged_df['high'], merged_df['low'], merged_df['close'], length=14)

    # True Strength Index (TSI)
    tsi = ta.tsi(merged_df['close'], long=25, short=13, signal=13)
    if isinstance(tsi, pd.DataFrame):
        merged_df['tsi'] = tsi.iloc[:, 0]
        merged_df['tsi_signal'] = tsi.iloc[:, 1]
    else:
        merged_df['tsi'] = tsi
        merged_df['tsi_signal'] = merged_df['tsi'].ewm(span=13).mean()

    # Заполнение пропущенных значений TSI
    merged_df[['tsi', 'tsi_signal']] = merged_df[['tsi', 'tsi_signal']].ffill()

    # Donchian Channel
    donchian = ta.donchian(
        high=merged_df['high'],
        low=merged_df['low'],
        lower_length=20,
        upper_length=20)
    merged_df['donchian_lower'] = donchian['DCL_20_20']
    merged_df['donchian_mid'] = donchian['DCM_20_20']
    merged_df['donchian_upper'] = donchian['DCU_20_20']

    # Дополнительные индикаторы
    merged_df['cci'] = ta.cci(merged_df['high'], merged_df['low'], merged_df['close'], length=20)
    merged_df['ulcer_index'] = ta.ui(merged_df['close'], length=14)

    return merged_df

def merge_and_calculate_metrics(df_candles, file_1, file_2, resample_interval, volatility_window):
    # Объединение данных
    merged_data = pd.merge_asof(
        file_1.sort_values('snapped_at'),
        file_2.sort_values('snapped_at'),
        on='snapped_at',
        direction='backward')

    # Переименование столбцов
    #print(merged_data.columns)
    merged_data.rename(columns={
        'snapped_at': 'timestamp',
        'market_cap_x': 'global_market_cap',
        'total_volume_x': 'global_total_volume',
        'price': 'close',
        'market_cap_y': 'bitcoin_market_cap',
        'total_volume_y': 'bitcoin_total_volume'
    }, inplace=True)

    merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'])

    # Расчет метрик
    merged_data['btc_dominance'] = (merged_data['bitcoin_market_cap'] / merged_data['global_market_cap']) * 100
    merged_data['btc_volume_dominance'] = (merged_data['bitcoin_total_volume'] / merged_data['global_total_volume']) * 100
    merged_data['btc_mc_to_vol'] = merged_data['bitcoin_market_cap'] / merged_data['bitcoin_total_volume']
    merged_data['global_mc_to_vol'] = merged_data['global_market_cap'] / merged_data['global_total_volume']
    merged_data['btc_price_to_mc'] = merged_data['close'] / merged_data['bitcoin_market_cap']
    merged_data['btc_volatility'] = merged_data['close'].rolling(window=volatility_window).std()
    merged_data.drop(columns='close', inplace=True)

    # Финальное объединение с основным датасетом
    merged_df = pd.merge_asof(
        df_candles.sort_values('timestamp'),
        merged_data.sort_values('timestamp'),
        on='timestamp',
        direction='backward')

    merged_df.set_index('timestamp', inplace=True)
    return merged_df
def create_and_train_model(df, freq_type):
    model = Prophet(
        seasonality_mode='multiplicative',
        changepoint_prior_scale=PREDEFINED_PARAMS["changepoint_prior_scale"],
        seasonality_prior_scale=PREDEFINED_PARAMS["seasonality_prior_scale"],
        yearly_seasonality=False
    )
    model.add_seasonality(name='yearly', period=365.25, fourier_order=PREDEFINED_PARAMS["yearly_fourier_order"])
    model.add_seasonality(name='weekly', period=7, fourier_order=PREDEFINED_PARAMS["weekly_fourier_order"])
    if freq_type == "H":
        model.add_seasonality(name='daily', period=1, fourier_order=PREDEFINED_PARAMS["daily_fourier_order"])
        model.add_seasonality(name='hourly', period=1/24, fourier_order=PREDEFINED_PARAMS["hourly_fourier_order"])
    if freq_type in ["H", "D"]:
        model.add_seasonality(name='monthly', period=30.44, fourier_order=PREDEFINED_PARAMS["monthly_fourier_order"])
    
    model.changepoint_range = PREDEFINED_PARAMS["changepoint_range"]

    # Добавляем праздники (пример для США)
    holidays = make_holidays_df(year_list=list(range(2017, datetime.now().year + 1)), country='US')
    model.holidays = holidays

    # Обучаем модель
    model.fit(df)
    return model
def make_forecast(model, new_data):
    """
    Делает прогноз на основе загруженной модели и нового набора данных.
    Параметры:
        model: Загруженная модель Prophet.
        new_data (pd.DataFrame): Новый набор данных с колонкой 'timestamp'.
    Возвращает:
        pd.DataFrame: Датасет с дополненными предсказаниями.
    """
    # Проверка, что колонка 'timestamp' существует
    if 'timestamp' not in new_data.columns:
        raise ValueError("The dataset must contain a 'timestamp' column.")

    # Преобразование колонки 'timestamp' в datetime
    new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
    new_data = new_data.sort_values('timestamp')

    # Создание датафрейма для предсказания
    future = new_data[['timestamp']].rename(columns={"timestamp": "ds"})
    forecast = model.predict(future)

    # Объединяем с исходным датасетом
    result = pd.merge(new_data, forecast, how="left", left_on="timestamp", right_on="ds")
    result.drop(columns=['ds'], inplace=True)
    return result 
def create_dataframe():
    symbol = f'{ticker}USDT'
    fgi_df = fetch_fgi()
    funding_df = fetch_funding_data(symbol)
 
    #datasets = {}

    #for tf_name, tf_interval in timeframes.items():
    #   print(f"Processing {tf_name} timeframe...")
    candle_data = fetch_candlestick_data(symbol, Client.KLINE_INTERVAL_1HOUR)
    
    merged_df = pd.merge_asof(
        pd.merge_asof(candle_data.sort_values(by='timestamp'), fgi_df, on='timestamp', direction='backward'),
        funding_df, on='timestamp', direction='backward')
    dataset = merged_df
    #print(f"Dataset for {tf_name} timeframe contains {len(merged_df)} records.")

# Сохранение результатов
#for tf_name, df in datasets.items():
#    file_name = f"dataset_{tf_name}.csv"
#    df.to_csv(file_name, index=False)
#    print(f"Dataset for {tf_name} saved as {file_name}.")  

    df_global=get_global_cap_and_volume()
    #df_global=df_global.drop(columns=['date'])
    df_btc=get_btc_cap_and_volume()
    #df_btc=df_btc.drop(columns=['timestamp'])
    #print(df_global.columns,df_btc.columns)

    merged_df = merge_and_calculate_metrics(dataset, df_global, df_btc, '1h', 24) #params['interval'], params['volatility_window'])
    
    # Расчёт индикаторов
    df = calculate_indicators(merged_df)

    # Убедимся, что индекс и столбцы корректны
    if 'timestamp' not in df.columns:
        df.reset_index(inplace=True)  # Восстанавливаем столбец `timestamp`
    # df.set_index('timestamp', inplace=True)  # Устанавливаем его обратно как индекс

    # Сохранение датасета в файл
    current_date = datetime.now().strftime('%d%m')
    #file_name = f"{ticker}_1h_{current_date}.csv"
    #df.to_csv(file_name, index=False)
    #print(f"Данные успешно сохранены в файл: {file_name}")
    
        # Параметры модели
    # PREDEFINED_PARAMS = {
    #  'changepoint_prior_scale': 0.4176933439369656, 
    #  'seasonality_prior_scale': 2.8272453308262318,
    #  'changepoint_range': 0.9499976369923773, 
    #  'yearly_fourier_order': 9, 
    #  'weekly_fourier_order': 10, 
    #  'daily_fourier_order': 9, 
    #  'hourly_fourier_order': 8, 
    #  'monthly_fourier_order': 8}
    
    df = df.sort_values('timestamp')
    prophet_df = df[['timestamp', 'close']].rename(columns={"timestamp": "ds", "close": "y"})
    # Определение типа частоты (пример для часов или дней)
    freq_type = "H"  # Можно определить автоматически, если требуется
    # Создание и обучение модели
    model = create_and_train_model(prophet_df, freq_type)
    result = make_forecast(model, df)
    #output_path = f"result_{ticker}_1h_{datetime.now().strftime('%d%m')}.csv"
    #result.to_csv(output_path, index=False)
    #print(f" result saved to {output_path}")
    df1=result.copy()
    df1=df1[['timestamp', 'open', 'high', 'low', 'close', 'volume',
       'quote_asset_volume', 'number_of_trades', 'taker_buy_base',
       'taker_buy_quote', 'FG', 'fundingRate', 'rsi', 'ema_20', 'ema_50',
       'ema_100', 'ema_200', 'sma_20', 'macd', 'macd_signal', 'macd_hist',
       'stochrsi', 'stochrsi_signal', 'stoch_k', 'stoch_d', 'roc', 'vwap',
       'kama', 'rma', 'hma_20', 'zlma_20', 'tema_20', 'trima_20', 'wma_20',
       'rsx', 'mad', 'bbands_high', 'bbands_low', 'dpo', 'kst', 'kst_signal',
       'ppo', 'ppo_signal', 'ppo_hist', 'rsi_6', 'trend_return', 'buy_volume',
       'sell_volume', 'delta', 'cumulative_delta', 'atr', 'adx', 'adx_pos',
       'adx_neg', 'chaikin', 'ad', 'mfi', 'williams_r', 'tsi', 'tsi_signal',
       'donchian_lower', 'donchian_mid', 'donchian_upper', 'cci',
       'ulcer_index', 'trend', 'yhat_lower', 'yhat_upper', 'trend_lower',
       'trend_upper','monthly', 'monthly_lower', 'monthly_upper', 'multiplicative_terms', 'multiplicative_terms_lower',
       'multiplicative_terms_upper', 'yearly', 'yearly_lower', 'yearly_upper','yhat']]
    df1 = df1.iloc[755:].reset_index(drop=True)
    df1 = df1.dropna().reset_index(drop=True)
    return df1


