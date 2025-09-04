# AI-Powered Stock Market Report Generator

A comprehensive Python application that generates detailed stock market reports using artificial intelligence. The program analyzes market data, news, and economic indicators to produce professional-grade market reports with insights on trends, opportunities, and risks.

## Features

- **AI-Powered Analysis**: Uses OpenAI GPT, Anthropic Claude, or Google Gemini for intelligent market analysis
- **Comprehensive Reports**: Generates 8 detailed sections covering all aspects of market analysis
- **Real-Time Data**: Fetches current market data, news, and economic indicators
- **Flexible Date Ranges**: Analyze any time period from one day up to one year
- **Multiple AI Agents**: Automatic fallback between different AI providers
- **Professional Output**: Generates markdown reports suitable for business use

## Report Sections

Each generated report includes:

1. **Executive Summary** - High-level market overview and key takeaways
2. **Global Market Overview** - Regional analysis and market size/growth
3. **Macro Trends & Drivers** - Technology, demographics, policy impacts
4. **Sector Highlights** - Performance analysis across major sectors
5. **Consumer Insights** - Spending patterns and behavioral trends
6. **Investment & Financial Outlook** - Market forecasts and recommendations
7. **Risks & Challenges** - Current threats and mitigation strategies
8. **Opportunities & Recommendations** - Growth prospects and strategic actions

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- At least one AI service API key (OpenAI, Anthropic, or Google)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/market-report-generator.git
cd market-report-generator
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
# Add at least one of these API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional: Enhanced news coverage
NEWS_API_KEY=your_newsapi_key_here

# Optional: Additional financial data
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

## API Key Setup

### OpenAI API Key
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Add to your `.env` file as `OPENAI_API_KEY`

### Anthropic Claude API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and generate an API key
3. Add to your `.env` file as `ANTHROPIC_API_KEY`

### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a project and generate an API key
3. Add to your `.env` file as `GOOGLE_API_KEY`

### Optional APIs
- **NewsAPI**: Get enhanced news coverage at [NewsAPI](https://newsapi.org/)
- **Alpha Vantage**: Additional financial data at [Alpha Vantage](https://www.alphavantage.co/)

## Usage

### Basic Usage

Generate a report for the past week (default):
```bash
python main.py
```

### Specify AI Agent

Use a specific AI agent:
```bash
python main.py --agent openai
python main.py --agent claude
python main.py --agent gemini
```

### Custom Date Range

Analyze a specific time period:
```bash
python main.py --start 2024-01-01 --end 2024-01-31
```

### Custom Output File

Save report with a specific filename:
```bash
python main.py --output my_report.md
```

### Verbose Logging

Enable detailed logging for troubleshooting:
```bash
python main.py --verbose
```

### Check Available Agents

See which AI agents are configured:
```bash
python main.py --check-keys
```

### Complete Example

```bash
python main.py --agent claude --start 2024-03-01 --end 2024-03-31 --output march_2024_report.md --verbose
```

## AI Agent Selection

The program automatically selects AI agents in this priority order:

1. **OpenAI GPT** (if API key available)
2. **Anthropic Claude** (if API key available)
3. **Google Gemini** (if API key available)

You can override this by specifying `--agent` parameter.

## Project Structure

```
market-report-generator/
├── main.py                 # Main application entry point
├── ai_agents.py           # AI agent integration
├── data_fetcher.py        # Market data and news fetching
├── report_generator.py    # Report generation logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Data Sources

The application fetches data from:

- **Yahoo Finance**: Stock prices, indices, economic indicators
- **Financial News RSS**: Reuters, Bloomberg, CNBC, MarketWatch
- **NewsAPI**: Enhanced news coverage (optional)
- **Alpha Vantage**: Additional financial data (optional)

## Example Output

Generated reports include:

```markdown
# COMPREHENSIVE STOCK MARKET REPORT
**Report Period:** 2024-03-01 to 2024-03-31
**Generated:** 2024-03-31 14:30:00
**AI Agent:** ['claude']

## EXECUTIVE SUMMARY
The stock market demonstrated resilience in March 2024, with major indices posting gains...

## GLOBAL MARKET OVERVIEW
Global markets showed mixed performance across regions...
```

## 🚨 Error Handling

The application includes comprehensive error handling for:

- Network connectivity issues
- API rate limits and errors
- Missing or invalid data
- File system permissions
- Invalid date ranges

## ⚡ Performance Tips

- **Date Range**: Shorter date ranges (1-30 days) generate faster
- **API Keys**: Having multiple AI agent keys provides redundancy
- **Internet**: Stable connection required for data fetching
- **Disk Space**: Reports are typically 5-50KB each

## 🔧 Troubleshooting

### Common Issues

**"No API keys configured"**
- Check your `.env` file exists and contains valid API keys
- Ensure `.env` is in the same directory as `main.py`

**"Error fetching market data"**
- Check your internet connection
- Some APIs have rate limits - try again later

**"AI agent failed to generate section"**
- Try a different AI agent with `--agent` parameter
- Check if your API key has sufficient credits/quota

**"Date range too large"**
- Maximum recommended range is 1 year
- Large ranges may timeout - try shorter periods

### Verbose Mode

Run with `--verbose` flag to see detailed logs:
```bash
python main.py --verbose
```

Logs are also saved to `market_report.log`.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Disclaimer

**Important**: This tool generates reports for informational purposes only. The analysis and recommendations should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

The accuracy of the generated reports depends on:
- Data source reliability
- AI model capabilities
- Market data availability
- News source accuracy

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs with `--verbose` flag
3. Ensure all API keys are valid and have sufficient quota
4. Check internet connectivity
5. Open an issue on GitHub with error details

## Future Enhancements

Planned features:
- HTML report generation
- Email report delivery
- Custom report templates
- Real-time alerts
- Portfolio analysis integration
- Additional data sources
- Web dashboard interface

---