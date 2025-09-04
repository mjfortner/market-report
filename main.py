#!/usr/bin/env python3
"""
Stock Market Report Generator
Main entry point for generating comprehensive stock market reports using AI agents
"""

import argparse
import logging
import sys
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from report_generator import MarketReportGenerator

# Load environment variables
load_dotenv()

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('market_report.log')
        ]
    )

def validate_date(date_string: str) -> datetime:
    """Validate and parse date string"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")

def get_default_date_range() -> tuple:
    """Get default date range (past week with emphasis on today)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def check_api_keys() -> list:
    """Check which API keys are available"""
    available_agents = []
    
    if os.getenv('OPENAI_API_KEY'):
        available_agents.append('openai')
    if os.getenv('ANTHROPIC_API_KEY'):
        available_agents.append('claude')
    if os.getenv('GOOGLE_API_KEY'):
        available_agents.append('gemini')
    
    return available_agents

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Generate comprehensive stock market reports using AI analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate report for past week
  %(prog)s --agent openai                     # Use OpenAI GPT specifically
  %(prog)s --start 2024-01-01 --end 2024-01-31  # Custom date range
  %(prog)s --output custom_report.md          # Custom output filename
  %(prog)s --verbose                          # Enable detailed logging
        """
    )
    
    parser.add_argument(
        '--agent',
        choices=['openai', 'claude', 'gemini'],
        help='Specify AI agent to use (default: auto-select based on available API keys)'
    )
    
    parser.add_argument(
        '--start',
        type=validate_date,
        help='Start date for analysis (YYYY-MM-DD). Default: 7 days ago'
    )
    
    parser.add_argument(
        '--end',
        type=validate_date,
        help='End date for analysis (YYYY-MM-DD). Default: today'
    )
    
    parser.add_argument(
        '--output',
        help='Output filename for the report (default: auto-generated with timestamp)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--check-keys',
        action='store_true',
        help='Check which API keys are configured and exit'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Check API keys if requested
    if args.check_keys:
        available = check_api_keys()
        if available:
            print(f"Available AI agents: {', '.join(available)}")
            print(f"Default priority order: openai -> claude -> gemini")
        else:
            print("No API keys configured. Please check your .env file.")
            print("Required: At least one of OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY")
        return
    
    # Check if any API keys are available
    available_agents = check_api_keys()
    if not available_agents:
        logging.error("No API keys configured. Please set up at least one API key in your .env file.")
        print("\nRequired environment variables (add to .env file):")
        print("- OPENAI_API_KEY=your_key_here")
        print("- ANTHROPIC_API_KEY=your_key_here") 
        print("- GOOGLE_API_KEY=your_key_here")
        print("\nCopy .env.example to .env and add your keys.")
        return 1
    
    # Validate agent selection
    if args.agent and args.agent not in available_agents:
        logging.error(f"Selected agent '{args.agent}' is not available. Available agents: {available_agents}")
        return 1
    
    # Set date range
    if args.start and args.end:
        start_date = args.start.strftime('%Y-%m-%d')
        end_date = args.end.strftime('%Y-%m-%d')
        
        if args.start >= args.end:
            logging.error("Start date must be before end date")
            return 1
            
        # Check if date range is too large
        if (args.end - args.start).days > 365:
            logging.warning("Date range is longer than 1 year. This may take a long time to process.")
    
    elif args.start or args.end:
        logging.error("Both --start and --end must be specified together")
        return 1
    
    else:
        start_date, end_date = get_default_date_range()
        logging.info(f"Using default date range: {start_date} to {end_date}")
    
    # Display configuration
    logging.info("=== Market Report Generator Configuration ===")
    logging.info(f"Date range: {start_date} to {end_date}")
    logging.info(f"Available agents: {available_agents}")
    logging.info(f"Selected agent: {args.agent or 'auto-select'}")
    logging.info("=" * 50)
    
    try:
        # Initialize report generator
        logging.info("Initializing AI agents...")
        generator = MarketReportGenerator(ai_agent=args.agent)
        
        # Generate report
        logging.info("Starting report generation...")
        logging.info("This may take several minutes depending on data availability and AI response time...")
        
        report = generator.generate_full_report(start_date, end_date)
        
        # Save report
        output_file = generator.save_report(report, args.output)
        
        if output_file:
            logging.info(f"Report successfully generated and saved to: {output_file}")
            print(f"\n✅ Market report generated successfully!")
            print(f"📄 Report saved to: {output_file}")
            print(f"📊 Analysis period: {start_date} to {end_date}")
            print(f"🤖 AI agent used: {generator.ai_manager.get_available_agents()}")
        else:
            logging.error("Failed to save report")
            return 1
    
    except KeyboardInterrupt:
        logging.info("Report generation cancelled by user")
        return 1
    
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        if args.verbose:
            logging.exception("Detailed error information:")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())