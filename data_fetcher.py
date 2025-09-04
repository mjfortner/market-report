"""
Data Fetching Module
Handles fetching stock market data, financial news, and economic indicators
"""

import os
import requests
import yfinance as yf
import pandas as pd
import feedparser
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class MarketDataFetcher:
    """Fetches market data from various sources"""
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    def get_market_indices(self, start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """Fetch major market indices data"""
        indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'Dow Jones': '^DJI',
            'Russell 2000': '^RUT',
            'VIX': '^VIX',
            'FTSE 100': '^FTSE',
            'Nikkei': '^N225',
            'Hang Seng': '^HSI'
        }
        
        data = {}
        for name, symbol in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    data[name] = hist
                    logging.info(f"Fetched data for {name}")
                else:
                    logging.warning(f"No data found for {name}")
            except Exception as e:
                logging.error(f"Error fetching {name}: {e}")
        
        return data
    
    def get_sector_performance(self, start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """Fetch sector ETF performance data"""
        sectors = {
            'Technology': 'XLK',
            'Healthcare': 'XLV',
            'Financial': 'XLF',
            'Consumer Discretionary': 'XLY',
            'Consumer Staples': 'XLP',
            'Energy': 'XLE',
            'Utilities': 'XLU',
            'Industrial': 'XLI',
            'Materials': 'XLB',
            'Real Estate': 'XLRE',
            'Communication': 'XLC'
        }
        
        data = {}
        for sector, symbol in sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    data[sector] = hist
                    logging.info(f"Fetched sector data for {sector}")
            except Exception as e:
                logging.error(f"Error fetching sector {sector}: {e}")
        
        return data
    
    def get_economic_indicators(self) -> Dict[str, float]:
        """Fetch key economic indicators"""
        indicators = {}
        
        try:
            # Treasury yields
            treasury_symbols = {
                '10Y Treasury': '^TNX',
                '2Y Treasury': '^IRX',
                '30Y Treasury': '^TYX'
            }
            
            for name, symbol in treasury_symbols.items():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d")
                if not hist.empty:
                    indicators[name] = hist['Close'].iloc[-1]
            
            # Dollar Index
            dxy = yf.Ticker('DX-Y.NYB')
            hist = dxy.history(period="5d")
            if not hist.empty:
                indicators['Dollar Index'] = hist['Close'].iloc[-1]
            
            # Gold and Oil
            gold = yf.Ticker('GC=F')
            hist = gold.history(period="5d")
            if not hist.empty:
                indicators['Gold'] = hist['Close'].iloc[-1]
            
            oil = yf.Ticker('CL=F')
            hist = oil.history(period="5d")
            if not hist.empty:
                indicators['Crude Oil'] = hist['Close'].iloc[-1]
                
        except Exception as e:
            logging.error(f"Error fetching economic indicators: {e}")
        
        return indicators
    
    def get_top_stocks_by_volume(self, date: str) -> List[Dict]:
        """Get top stocks by trading volume"""
        try:
            # Get S&P 500 components
            sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(sp500_url)
            sp500_symbols = tables[0]['Symbol'].tolist()
            
            # Sample a subset for performance
            import random
            sample_symbols = random.sample(sp500_symbols, min(50, len(sp500_symbols)))
            
            volume_data = []
            for symbol in sample_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        volume_data.append({
                            'symbol': symbol,
                            'volume': hist['Volume'].iloc[-1],
                            'price': hist['Close'].iloc[-1],
                            'change': ((hist['Close'].iloc[-1] - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1]) * 100
                        })
                except:
                    continue
            
            # Sort by volume and return top 10
            volume_data.sort(key=lambda x: x['volume'], reverse=True)
            return volume_data[:10]
            
        except Exception as e:
            logging.error(f"Error fetching top stocks: {e}")
            return []

class NewsDataFetcher:
    """Fetches financial news and market-related information"""
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
    
    def get_financial_news(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch financial news from various sources"""
        news_articles = []
        
        # RSS feeds for financial news
        rss_feeds = [
            'https://feeds.reuters.com/reuters/businessNews',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
            'https://feeds.marketwatch.com/marketwatch/topstories/',
            'https://finance.yahoo.com/rss/'
        ]
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', 'Unknown'),
                        'summary': entry.get('summary', entry.get('description', '')),
                        'source': feed.feed.get('title', 'Unknown')
                    }
                    news_articles.append(article)
            except Exception as e:
                logging.warning(f"Error fetching from RSS feed {feed_url}: {e}")
        
        # Use News API if available
        if self.news_api_key:
            try:
                news_articles.extend(self._fetch_from_news_api(start_date, end_date))
            except Exception as e:
                logging.warning(f"Error fetching from News API: {e}")
        
        return news_articles
    
    def _fetch_from_news_api(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch news from News API"""
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'stock market OR economy OR finance OR trading OR investment',
            'from': start_date,
            'to': end_date,
            'sortBy': 'relevancy',
            'language': 'en',
            'pageSize': 50,
            'apiKey': self.news_api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        articles = []
        data = response.json()
        
        for article in data.get('articles', []):
            articles.append({
                'title': article['title'],
                'link': article['url'],
                'published': article['publishedAt'],
                'summary': article['description'],
                'source': article['source']['name']
            })
        
        return articles
    
    def get_market_sentiment_indicators(self) -> Dict[str, any]:
        """Get market sentiment indicators"""
        sentiment = {}
        
        try:
            # VIX (Fear & Greed Index)
            vix = yf.Ticker('^VIX')
            vix_hist = vix.history(period="5d")
            if not vix_hist.empty:
                current_vix = vix_hist['Close'].iloc[-1]
                sentiment['VIX'] = current_vix
                
                if current_vix < 20:
                    sentiment['VIX_interpretation'] = 'Low volatility - Complacent market'
                elif current_vix < 30:
                    sentiment['VIX_interpretation'] = 'Moderate volatility - Normal market conditions'
                else:
                    sentiment['VIX_interpretation'] = 'High volatility - Fearful market'
            
            # Put/Call Ratio would require additional data source
            # Market breadth indicators
            spy = yf.Ticker('SPY')
            spy_hist = spy.history(period="30d")
            if not spy_hist.empty:
                # Simple trend analysis
                recent_avg = spy_hist['Close'].tail(5).mean()
                older_avg = spy_hist['Close'].head(5).mean()
                trend = "Bullish" if recent_avg > older_avg else "Bearish"
                sentiment['SPY_trend'] = trend
                
        except Exception as e:
            logging.error(f"Error fetching sentiment indicators: {e}")
        
        return sentiment

class DataProcessor:
    """Processes and analyzes fetched data"""
    
    @staticmethod
    def calculate_performance_metrics(data: pd.DataFrame) -> Dict[str, float]:
        """Calculate basic performance metrics"""
        if data.empty:
            return {}
        
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        high_price = data['High'].max()
        low_price = data['Low'].min()
        
        return {
            'total_return': ((end_price - start_price) / start_price) * 100,
            'high': high_price,
            'low': low_price,
            'volatility': data['Close'].pct_change().std() * 100,
            'avg_volume': data['Volume'].mean()
        }
    
    @staticmethod
    def identify_trends(data: pd.DataFrame, window: int = 20) -> Dict[str, str]:
        """Identify market trends"""
        if len(data) < window:
            return {'trend': 'Insufficient data'}
        
        # Simple moving average trend
        data['SMA'] = data['Close'].rolling(window=window).mean()
        current_price = data['Close'].iloc[-1]
        current_sma = data['SMA'].iloc[-1]
        
        if current_price > current_sma:
            trend = 'Uptrend'
        else:
            trend = 'Downtrend'
        
        # Momentum
        price_change = data['Close'].pct_change(window).iloc[-1] * 100
        
        return {
            'trend': trend,
            'momentum': f"{price_change:.2f}% over {window} days"
        }