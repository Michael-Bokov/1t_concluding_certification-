
import logging
import pandas as pd
import pandas_ta as ta
import pytz
import requests
import schedule
from datetime import datetime, timedelta
import time
from schemas import CandlestickData_f,TechnicalIndicators_f
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

pd.set_option('display.max_columns', None)
# Устанавливаем опцию, чтобы выводить все строки (если нужно)
pd.set_option('display.max_rows', None)
# Устанавливаем опцию для более широкой ширины вывода
pd.set_option('display.width', 1000)


logging.basicConfig(filename='btcloader_1h_futures.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
engine = create_engine('postgresql://fintech_admin:admin@db:5432/FinTech6_BTC')
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
candlestick_table = Table('candles_1h_fut', metadata, autoload_with=engine)

def save_candlestick_data(df):
    try:
        candles = []
        indicators = []
        for _, row in df.iterrows():
            #timestamp_utc = pd.to_datetime(row['timestamp'], unit='ms', utc=True)
            candle = CandlestickData_f(
                timestamp=datetime.utcfromtimestamp(row['timestamp'] / 1000.0).replace(microsecond=0),#row['timestamp'],#timestamp_utc,
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                quote_asset_volume=row['quote_asset_volume'],
                number_of_trades=row['number_of_trades'],
                taker_buy_base_asset_volume=row['taker_buy_base_asset_volume'],
                taker_buy_quote_asset_volume=row['taker_buy_quote_asset_volume']
            )
            session.add(candle)
            session.flush()  # Присваивание ID для индикатора

            indicator = TechnicalIndicators_f(
                candlestick_id=candle.id,
                timestamp=datetime.utcfromtimestamp(row['timestamp'] / 1000.0).replace(microsecond=0),#row['timestamp'],
                openinterest=row['openinterest'],
                openinterest_value=row['openinterest_value'],
                rsi=row['RSI'],
                ema_20=row['EMA_20'],
                ema_50=row['EMA_50'],
                macd=row['MACD'],
                macd_signal=row['MACD_signal'],
                macd_hist=row['MACD_hist'],
                stoch_k=row['Stoch_K'],
                stoch_d=row['Stoch_D'],
                roc=row['ROC'],
                vwap=row['VWAP'],
                macd_21_34_1=row['MACD_21_34_1'],
                macd_signal_21_34_1=row['MACD_signal_21_34_1'],
                macd_hist_21_34_1=row['MACD_hist_21_34_1'],
                macd_31_144_1=row['MACD_31_144_1'],
                macd_signal_31_144_1=row['MACD_signal_31_144_1'],
                macd_hist_31_144_1=row['MACD_hist_31_144_1'],
                tsi=row['tsi'],
                tsi_signal=row['tsi_signal'],
                rsi_o=row['rsi_o'],
                sma_20=row['sma_20'],
                ema_100=row['ema_100'],
                ema_200=row['ema_200'],
                wma_20=row['wma_20'],
                hma_20=row['hma_20'],
                zlma_20=row['zlma_20'],
                tema_20=row['tema_20'],
                trima_20=row['trima_20'],
                stochrsi=row['stochrsi'],
                stochrsi_signal=row['stochrsi_signal'],
                kama=row['kama'],
                rma=row['rma'],
                rsi_sma=row['rsi_sma'],
                rsx=row['rsx'],
                mad=row['mad'],
                bbands_high=row['bbands_high'],
                bbands_low=row['bbands_low'],
                dpo=row['dpo'],
                kst=row['kst'],
                kst_signal=row['kst_signal'],
                rsi_6=row['rsi_6'],
                ppo=row['ppo'],
                ppo_signal=row['ppo_signal'],
                ppo_hist=row['ppo_hist'],
                trend_return=row['trend_return']

            )
            indicators.append(indicator)
        session.bulk_save_objects(indicators)  # Сохраняем все индикаторы за один раз
        session.commit()
        logging.info("Data saved successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error saving data: {str(e)}")
def get_last_timestamp():
    try:
        # Получаем последний временной stemp из базы данных
        last_candle = session.query(CandlestickData_f).order_by(CandlestickData_f.timestamp.desc()).first()
        if last_candle:
            return last_candle.timestamp
        else:
            return None  # Если данных нет, возвращаем None
    except SQLAlchemyError as e:
        logging.error(f"Error fetching last timestamp: {str(e)}")
        return None

def fetch_last_n_rows(n):
    with engine.connect() as connection:
         query = select(candlestick_table).order_by(candlestick_table.c.timestamp.desc()).limit(n)

         result = connection.execute(query)
         df = pd.DataFrame(result.fetchall(), columns=result.keys())
         df = df.sort_values(by='timestamp')  # Сортируем по возрастанию времени
         return df
# Функция для загрузки данных с Binance API
def get_klines_iter(symbol, interval, start, end=None, limit=500):
    df_full = fetch_last_n_rows(201) #pd.DataFrame()
    df = pd.DataFrame()
    while True:
        url = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}&startTime={int(start)}'
        url_open_interest = f"https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period={interval}"
        #print(url_open_interest)
        if end:
            url += f'&endTime={int(end)}'
        df2 = pd.read_json(url)
        if df2.empty:
            break
        # GET-запрос для Open Interest
        #response_oi = requests.get(url_open_interest)

        #if response_oi.status_code == 200:
        df_oi = pd.read_json(url_open_interest) # Получение данных в формате JSON
        df_oi.columns=['symbol', 'openinterest', 'openinterest_value', 'timestamp']
        df_oi = df_oi.drop(columns=['symbol'])
        #print(df_oi.head(50))
        nc=['openinterest','openinterest_value']
        df_oi[nc]= df_oi[nc].astype(float)

        df_oi['timestamp'] = pd.to_datetime(df_oi['timestamp'], unit='ms', utc=True).dt.floor('s')

        df2.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'closetime',
                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                       'taker_buy_quote_asset_volume', 'ignore']
        df2 = df2.drop(columns=['closetime', 'ignore'])
        numeric_columns = ['open', 'high', 'low', 'close', 'volume',
                           'quote_asset_volume', 'number_of_trades',
                           'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']

        df2['timestamp'] = pd.to_datetime(df2['timestamp'], unit='ms', utc=True).dt.floor('s')

        df2[numeric_columns] = df2[numeric_columns].astype(float)
        df = pd.concat([df, df2], axis=0, ignore_index=True, keys=None)
        #df = df.merge(df_oi[['timestamp', 'openinterest', 'openinterest_value']], on='timestamp', how='left')
        # Прерывание при достижении конца данных
        #if len(df2) < limit:
        #    break
        start = df2.iloc[-1]['timestamp'] + pd.Timedelta(milliseconds=1)
        start=start.timestamp()*1000
        #print(type(start))
        time.sleep(0.2)  # Чтобы избежать слишком частых запросов
    if not df.empty:

        df_full = pd.concat([df_full, df], axis=0, ignore_index=True, keys=None)
        df_full=df_full.drop(columns=['id'])

        df_full.drop_duplicates(subset='timestamp', keep='first', inplace=True)
        if df_full['timestamp'].dtype == 'object':
            try:
                # Если значения в timestamp в строковом формате, преобразуем их в миллисекунды
                df_full['timestamp'] = pd.to_datetime(df_full['timestamp'], utc=True)
                df_full['timestamp'] = df_full['timestamp'].view('int64') // 10 ** 6  # Преобразуем в миллисекунды
            except ValueError as e:
                print(f"Error converting timestamp: {e}")

                #Убедиться, что столбец с временными метками существует и преобразован в datetime
        df_full['tc'] = pd.to_datetime(df_full['timestamp'])#,unit="ms",utc=True)
        df_full.set_index('tc', inplace=True)
        df_full = df_full[~df_full.index.duplicated(keep='first')]

        df_full[numeric_columns] = df_full[numeric_columns].astype(float)

        df_full['RSI'] = ta.rsi(df_full['close'], length=14, mamode='sma')
        df_full['EMA_20'] = ta.ema(df_full['close'], length=20)
        df_full['EMA_50'] = ta.ema(df_full['close'], length=50)

        macd = ta.macd(df_full['close'], fast=12, slow=26, signal=9)
        df_full['MACD'] = macd['MACD_12_26_9']
        df_full['MACD_signal'] = macd['MACDs_12_26_9']
        df_full['MACD_hist'] = macd['MACDh_12_26_9']

        stoch = ta.stoch(df_full['high'], df_full['low'], df_full['close'], k=14, d=3)
        df_full['Stoch_K'] = stoch['STOCHk_14_3_3']
        df_full['Stoch_D'] = stoch['STOCHd_14_3_3']

        df_full['ROC'] = ta.roc(df_full['close'], length=14)
        df_full['VWAP'] = ta.vwap(df_full['high'], df_full['low'], df_full['close'], df_full['volume'])

        macd_21_34_1 = ta.macd(df_full['close'], fast=21, slow=34, signal=1)
        df_full['MACD_21_34_1'] = macd_21_34_1['MACD_21_34_1']
        df_full['MACD_signal_21_34_1'] = macd_21_34_1['MACDs_21_34_1']
        df_full['MACD_hist_21_34_1'] = macd_21_34_1['MACDh_21_34_1']
        if len(df_full)>143:
            macd_31_144_1 = ta.macd(df_full['close'], fast=31, slow=144, signal=1)
            df_full['MACD_31_144_1'] = macd_31_144_1['MACD_31_144_1']
            df_full['MACD_signal_31_144_1'] = macd_31_144_1['MACDs_31_144_1']
            df_full['MACD_hist_31_144_1'] = macd_31_144_1['MACDh_31_144_1']

        df_full[['tsi', 'tsi_signal']] = ta.tsi(close=df_full['close'], length=25)
        df_full['rsi_o'] = ta.rsi(df_full['close'], lenght=14)
        df_full['sma_20'] = ta.sma(df_full['close'], length=20)
        df_full['ema_100'] = ta.ema(df_full['close'], length=100)  # EMA(100)
        df_full['ema_200'] = ta.ema(df_full['close'], length=200)  # EMA(200)
        df_full['wma_20'] = ta.wma(df_full['close'], length=20)
        df_full['hma_20'] = ta.hma(df_full['close'], length=20)
        df_full['zlma_20'] = ta.zlma(df_full['close'], length=20)
        df_full['tema_20'] = ta.tema(df_full['close'], length=20)
        df_full['trima_20'] = ta.trima(df_full['close'], length=20)
        # df['pvo'] = ta.pvo(close=df['close'], short_length=12, long_length=26)  # PVO (percentage volume oscillator)
        df_full[['stochrsi', 'stochrsi_signal']] = ta.stochrsi(df_full['close'], length=14)
        df_full['kama'] = ta.kama(df_full['close'], length=10)
        df_full['rma'] = ta.rma(df_full['close'], length=20)
        df_full['rsi_sma'] = ta.rsi(df_full['close'], length=20, talib=True)
        df_full['rsx'] = ta.rsx(df_full['close'], length=14)
        df_full['mad'] = ta.mad(df_full['close'], length=14)
        df_full['bbands_high'], df_full['bbands_low'] = ta.bbands(df_full['close'], length=20)[['BBU_20_2.0', 'BBL_20_2.0']].T.values
        df_full['dpo'] = ta.dpo(close=df_full['close'], length=20)  # для устранения долгосрочного тренда.
        df_full[['kst', 'kst_signal']] = ta.kst(close=df_full['close'], length=14)  # индикатор импульса. Know Sure Thing
        # df['vortex'] = ta.vortex(close=df['close'],length=14)         # для определения разворотов тренда
        df_full['rsi_6'] = ta.rsi(df_full['close'], length=6)  # RSI с другой длиной
        # df['cci'] = ta.cci(df['close'], length=20)  # Commodity Channel Index
        df_full[['ppo', 'ppo_signal', 'ppo_hist']] = ta.ppo(df_full['close'])  # Percentage Price Oscillator
        df_full['trend_return'] = ta.percent_return(df_full['close'], length=20)

        df_oi['timestamp'] = df_oi['timestamp'].view('int64') // 10 ** 6
        df_full = df_full.merge(df_oi[['timestamp', 'openinterest', 'openinterest_value']], on='timestamp', how='left')
        df_full.reset_index(drop=True, inplace=True)
        #print(df.shape)
        df=df_full
    return df
def fetch_and_calculate():
    symbol = 'BTCUSDT'
    interval = '1h'

    last_timestamp = get_last_timestamp()
    if last_timestamp.tzinfo is None:
        last_timestamp = last_timestamp.replace(tzinfo=pytz.UTC)
    else:
        last_timestamp = last_timestamp.astimezone(pytz.UTC)

    start_timestamp = int(last_timestamp.timestamp() * 1000)  # Convert to milliseconds
    print(f"Last date in database: {last_timestamp}, Start timestamp: {start_timestamp}")

    # Current date and timestamp
    now = datetime.utcnow()
    end_timestamp = int(now.timestamp() * 1000)  # Convert to milliseconds

    df_new = get_klines_iter(symbol, interval, start_timestamp, end_timestamp)
    df_new = df_new.iloc[201:]

    # Process new data
    if not df_new.empty:
        save_candlestick_data(df_new)
        print(f"Data updated, new rows: {len(df_new)}")
    else:
        print("No new data to append.")
# Планирование задачи каждые 30 минут
schedule.every(30).minutes.do(fetch_and_calculate)

while True:
    schedule.run_pending()
    time.sleep(1)
