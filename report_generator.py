"""
Market Report Generator
Generates comprehensive market reports using AI analysis
"""

from datetime import datetime, timedelta
import logging
import json
from typing import Dict, List, Optional
from ai_agents import AIAgentManager
from data_fetcher import MarketDataFetcher, NewsDataFetcher, DataProcessor

class MarketReportGenerator:
    """Main class for generating market reports"""
    
    def __init__(self, ai_agent: str = None):
        self.ai_manager = AIAgentManager(ai_agent)
        self.market_fetcher = MarketDataFetcher()
        self.news_fetcher = NewsDataFetcher()
        self.processor = DataProcessor()
        
    def generate_full_report(self, start_date: str, end_date: str) -> str:
        """Generate a complete market report"""
        logging.info(f"Generating market report from {start_date} to {end_date}")
        
        # Fetch all required data
        market_data = self._fetch_market_data(start_date, end_date)
        news_data = self._fetch_news_data(start_date, end_date)
        
        # Generate each section
        report_sections = []
        
        report_sections.append(self._generate_executive_summary(market_data, news_data))
        report_sections.append(self._generate_global_market_overview(market_data))
        report_sections.append(self._generate_macro_trends(market_data, news_data))
        report_sections.append(self._generate_sector_highlights(market_data))
        report_sections.append(self._generate_consumer_insights(news_data))
        report_sections.append(self._generate_investment_outlook(market_data))
        report_sections.append(self._generate_risks_challenges(market_data, news_data))
        report_sections.append(self._generate_opportunities_recommendations(market_data, news_data))
        
        # Combine all sections
        full_report = self._format_final_report(report_sections, start_date, end_date)
        
        return full_report
    
    def _fetch_market_data(self, start_date: str, end_date: str) -> Dict:
        """Fetch all market-related data"""
        data = {
            'indices': self.market_fetcher.get_market_indices(start_date, end_date),
            'sectors': self.market_fetcher.get_sector_performance(start_date, end_date),
            'economic_indicators': self.market_fetcher.get_economic_indicators(),
            'top_stocks': self.market_fetcher.get_top_stocks_by_volume(end_date),
            'sentiment': self.news_fetcher.get_market_sentiment_indicators()
        }
        return data
    
    def _fetch_news_data(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch news and sentiment data"""
        return self.news_fetcher.get_financial_news(start_date, end_date)
    
    def _generate_executive_summary(self, market_data: Dict, news_data: List[Dict]) -> str:
        """Generate executive summary section"""
        # Prepare data summary
        indices_summary = self._summarize_indices_performance(market_data['indices'])
        sentiment_summary = market_data['sentiment']
        
        prompt = """
        Create an Executive Summary for a stock market report. Include:
        1. Overall economic climate assessment
        2. High-level opportunities and risks across markets
        3. Key takeaways for investors and businesses
        
        Make it concise but comprehensive, suitable for C-level executives.
        """
        
        data_context = f"""
        Market Indices Performance: {indices_summary}
        Market Sentiment: {sentiment_summary}
        Recent News Headlines: {[article['title'] for article in news_data[:10]]}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_global_market_overview(self, market_data: Dict) -> str:
        """Generate global market overview section"""
        indices_data = market_data['indices']
        economic_indicators = market_data['economic_indicators']
        
        prompt = """
        Create a Global Market Overview section that covers:
        1. Current size and growth of global economy
        2. Key regions driving growth (North America, Asia-Pacific, Europe)
        3. Broad market segmentation analysis
        4. Cross-regional market correlations and trends
        """
        
        data_context = f"""
        Major Indices Performance:
        {self._format_indices_data(indices_data)}
        
        Economic Indicators:
        {json.dumps(economic_indicators, indent=2)}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_macro_trends(self, market_data: Dict, news_data: List[Dict]) -> str:
        """Generate macro trends and drivers section"""
        prompt = """
        Analyze and describe Macro Trends & Drivers affecting markets:
        1. Technology trends (AI, automation, digitalization)
        2. Demographics (population shifts, urbanization, aging)
        3. Environment & sustainability (climate policies, ESG focus)
        4. Regulation & policy changes (trade, tariffs, taxes)
        
        Focus on how these trends are currently impacting markets.
        """
        
        # Extract technology and policy-related news
        relevant_news = [article for article in news_data if any(keyword in article['title'].lower() 
                        for keyword in ['technology', 'ai', 'regulation', 'policy', 'climate', 'esg'])]
        
        data_context = f"""
        Market Performance Data: {self._summarize_indices_performance(market_data['indices'])}
        Relevant News: {[article['title'] + ' - ' + article['summary'] for article in relevant_news[:15]]}
        Economic Indicators: {market_data['economic_indicators']}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_sector_highlights(self, market_data: Dict) -> str:
        """Generate sector highlights section"""
        sectors_data = market_data['sectors']
        
        prompt = """
        Provide Sector Highlights covering:
        1. Performance analysis of major sectors (Technology, Healthcare, Financial, etc.)
        2. Which sectors are expanding, contracting, or transforming
        3. Sector rotation trends and implications
        4. Key sector-specific opportunities and challenges
        """
        
        data_context = f"""
        Sector Performance Data:
        {self._format_sectors_data(sectors_data)}
        
        Top Volume Stocks: {market_data['top_stocks']}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_consumer_insights(self, news_data: List[Dict]) -> str:
        """Generate consumer insights section"""
        prompt = """
        Analyze Consumer Insights based on market data and news:
        1. Shifts in consumer confidence and spending patterns
        2. Behavioral changes (digital adoption, value-seeking, brand loyalty)
        3. Impact on retail and consumer-facing sectors
        4. Implications for businesses and investors
        """
        
        # Filter consumer-related news
        consumer_news = [article for article in news_data if any(keyword in article['title'].lower() 
                        for keyword in ['consumer', 'retail', 'spending', 'confidence', 'inflation'])]
        
        data_context = f"""
        Consumer-Related News:
        {[article['title'] + ' - ' + article['summary'] for article in consumer_news[:20]]}
        
        All Recent Headlines: {[article['title'] for article in news_data[:30]]}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_investment_outlook(self, market_data: Dict) -> str:
        """Generate investment and financial outlook section"""
        prompt = """
        Provide Investment & Financial Outlook covering:
        1. Market confidence and risk appetite assessment
        2. Capital flows and investment trends
        3. Financial forecasts (GDP growth expectations, inflation outlook, interest rate trends)
        4. Asset allocation recommendations
        """
        
        data_context = f"""
        Market Performance: {self._summarize_indices_performance(market_data['indices'])}
        Economic Indicators: {market_data['economic_indicators']}
        Market Sentiment: {market_data['sentiment']}
        Volatility Analysis: {self._analyze_volatility(market_data['indices'])}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_risks_challenges(self, market_data: Dict, news_data: List[Dict]) -> str:
        """Generate risks and challenges section"""
        prompt = """
        Identify and analyze Risks & Challenges:
        1. Global risks (geopolitical tensions, supply chain disruptions, inflationary pressures)
        2. Industry-agnostic business risks (cybersecurity, labor shortages)
        3. Market-specific risks and vulnerabilities
        4. Risk mitigation strategies
        """
        
        # Filter risk-related news
        risk_news = [article for article in news_data if any(keyword in article['title'].lower() 
                    for keyword in ['risk', 'crisis', 'tension', 'inflation', 'recession', 'cyber', 'supply chain'])]
        
        data_context = f"""
        Risk-Related News:
        {[article['title'] + ' - ' + article['summary'] for article in risk_news[:20]]}
        
        Market Volatility: {market_data['sentiment'].get('VIX', 'N/A')}
        Market Trends: {self._analyze_market_trends(market_data['indices'])}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _generate_opportunities_recommendations(self, market_data: Dict, news_data: List[Dict]) -> str:
        """Generate opportunities and recommendations section"""
        prompt = """
        Provide Opportunities & Recommendations:
        1. Growth opportunities across regions and sectors
        2. Strategic actions for businesses (innovation, diversification, partnerships)
        3. Investment recommendations for different risk profiles
        4. Emerging market opportunities and trends to watch
        """
        
        # Filter opportunity-related news
        opportunity_news = [article for article in news_data if any(keyword in article['title'].lower() 
                           for keyword in ['growth', 'opportunity', 'innovation', 'merger', 'acquisition', 'ipo'])]
        
        data_context = f"""
        Market Performance Trends: {self._analyze_market_trends(market_data['indices'])}
        Sector Performance: {self._format_sectors_data(market_data['sectors'])}
        Top Performing Stocks: {market_data['top_stocks'][:10]}
        Opportunity-Related News:
        {[article['title'] + ' - ' + article['summary'] for article in opportunity_news[:15]]}
        """
        
        return self.ai_manager.generate_report_section(prompt, data_context)
    
    def _summarize_indices_performance(self, indices_data: Dict) -> Dict:
        """Summarize performance of major indices"""
        summary = {}
        for name, data in indices_data.items():
            if not data.empty:
                metrics = self.processor.calculate_performance_metrics(data)
                summary[name] = metrics
        return summary
    
    def _format_indices_data(self, indices_data: Dict) -> str:
        """Format indices data for AI consumption"""
        formatted = []
        for name, data in indices_data.items():
            if not data.empty:
                metrics = self.processor.calculate_performance_metrics(data)
                formatted.append(f"{name}: {metrics}")
        return '\n'.join(formatted)
    
    def _format_sectors_data(self, sectors_data: Dict) -> str:
        """Format sector data for AI consumption"""
        formatted = []
        for sector, data in sectors_data.items():
            if not data.empty:
                metrics = self.processor.calculate_performance_metrics(data)
                formatted.append(f"{sector}: {metrics}")
        return '\n'.join(formatted)
    
    def _analyze_volatility(self, indices_data: Dict) -> Dict:
        """Analyze market volatility"""
        volatility = {}
        for name, data in indices_data.items():
            if not data.empty and len(data) > 1:
                daily_returns = data['Close'].pct_change().dropna()
                volatility[name] = {
                    'daily_volatility': daily_returns.std() * 100,
                    'annualized_volatility': daily_returns.std() * (252 ** 0.5) * 100
                }
        return volatility
    
    def _analyze_market_trends(self, indices_data: Dict) -> Dict:
        """Analyze market trends across indices"""
        trends = {}
        for name, data in indices_data.items():
            if not data.empty:
                trends[name] = self.processor.identify_trends(data)
        return trends
    
    def _format_final_report(self, sections: List[str], start_date: str, end_date: str) -> str:
        """Format the final report with proper structure"""
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# COMPREHENSIVE STOCK MARKET REPORT
**Report Period:** {start_date} to {end_date}
**Generated:** {report_date}
**AI Agent:** {self.ai_manager.get_available_agents()}

---

## EXECUTIVE SUMMARY
{sections[0]}

---

## GLOBAL MARKET OVERVIEW
{sections[1]}

---

## MACRO TRENDS & DRIVERS
{sections[2]}

---

## SECTOR HIGHLIGHTS
{sections[3]}

---

## CONSUMER INSIGHTS
{sections[4]}

---

## INVESTMENT & FINANCIAL OUTLOOK
{sections[5]}

---

## RISKS & CHALLENGES
{sections[6]}

---

## OPPORTUNITIES & RECOMMENDATIONS
{sections[7]}

---

## METHODOLOGY & DATA SOURCES
This report was generated using AI analysis of:
- Real-time market data from Yahoo Finance
- Financial news from multiple RSS feeds and news APIs
- Economic indicators and market sentiment data
- Sector performance and individual stock analysis

**Disclaimer:** This report is for informational purposes only and should not be considered as investment advice. Always consult with qualified financial advisors before making investment decisions.

---
*Report generated by AI-Powered Market Report Generator*
"""
        return report
    
    def save_report(self, report: str, filename: str = None) -> str:
        """Save report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_report_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            logging.info(f"Report saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving report: {e}")
            return None