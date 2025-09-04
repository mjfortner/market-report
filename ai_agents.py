"""
AI Agent Integration Module
Handles communication with OpenAI, Anthropic Claude, and Google Gemini APIs
"""

import os
from typing import Optional, Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAgent:
    """Base class for AI agents"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
    
    def generate_report_section(self, prompt: str, data: str) -> str:
        """Generate a report section based on prompt and data"""
        raise NotImplementedError

class OpenAIAgent(AIAgent):
    """OpenAI GPT integration"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def generate_report_section(self, prompt: str, data: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a financial analyst creating comprehensive market reports. Provide detailed, professional analysis."},
                    {"role": "user", "content": f"{prompt}\n\nData to analyze:\n{data}"}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return f"Error generating section: {str(e)}"

class ClaudeAgent(AIAgent):
    """Anthropic Claude integration"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")
    
    def generate_report_section(self, prompt: str, data: str) -> str:
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": f"You are a financial analyst creating comprehensive market reports. Provide detailed, professional analysis.\n\n{prompt}\n\nData to analyze:\n{data}"}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logging.error(f"Claude API error: {e}")
            return f"Error generating section: {str(e)}"

class GeminiAgent(AIAgent):
    """Google Gemini integration"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-pro')
        except ImportError:
            raise ImportError("Google Generative AI library not installed. Run: pip install google-generativeai")
    
    def generate_report_section(self, prompt: str, data: str) -> str:
        try:
            full_prompt = f"You are a financial analyst creating comprehensive market reports. Provide detailed, professional analysis.\n\n{prompt}\n\nData to analyze:\n{data}"
            response = self.client.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            return f"Error generating section: {str(e)}"

class AIAgentManager:
    """Manages AI agent selection and fallback logic"""
    
    def __init__(self, preferred_agent: Optional[str] = None):
        self.agents = {}
        self.preferred_agent = preferred_agent
        self.current_agent = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize available AI agents based on API keys"""
        # Check for API keys and initialize agents
        openai_key = os.getenv('OPENAI_API_KEY')
        claude_key = os.getenv('ANTHROPIC_API_KEY')
        gemini_key = os.getenv('GOOGLE_API_KEY')
        
        if openai_key:
            try:
                self.agents['openai'] = OpenAIAgent(openai_key)
                logging.info("OpenAI agent initialized")
            except Exception as e:
                logging.warning(f"Failed to initialize OpenAI agent: {e}")
        
        if claude_key:
            try:
                self.agents['claude'] = ClaudeAgent(claude_key)
                logging.info("Claude agent initialized")
            except Exception as e:
                logging.warning(f"Failed to initialize Claude agent: {e}")
        
        if gemini_key:
            try:
                self.agents['gemini'] = GeminiAgent(gemini_key)
                logging.info("Gemini agent initialized")
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini agent: {e}")
        
        if not self.agents:
            raise ValueError("No AI agents could be initialized. Please check your API keys in the .env file.")
        
        # Set current agent based on preference or default priority
        self._set_current_agent()
    
    def _set_current_agent(self):
        """Set the current agent based on preference and availability"""
        if self.preferred_agent and self.preferred_agent in self.agents:
            self.current_agent = self.agents[self.preferred_agent]
            logging.info(f"Using preferred agent: {self.preferred_agent}")
            return
        
        # Default priority: OpenAI -> Claude -> Gemini
        priority = ['openai', 'claude', 'gemini']
        for agent_name in priority:
            if agent_name in self.agents:
                self.current_agent = self.agents[agent_name]
                logging.info(f"Using default agent: {agent_name}")
                return
    
    def generate_report_section(self, prompt: str, data: str) -> str:
        """Generate a report section using the current agent"""
        if not self.current_agent:
            return "Error: No AI agent available"
        
        return self.current_agent.generate_report_section(prompt, data)
    
    def get_available_agents(self) -> list:
        """Return list of available agent names"""
        return list(self.agents.keys())
    
    def switch_agent(self, agent_name: str) -> bool:
        """Switch to a different agent"""
        if agent_name in self.agents:
            self.current_agent = self.agents[agent_name]
            logging.info(f"Switched to agent: {agent_name}")
            return True
        return False