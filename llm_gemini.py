import os
import requests
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables
load_dotenv()

class GeminiAPI:
    def __init__(self):
        """Initialize Gemini API client"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    def analyze_topic(self, topic: str, custom_prompt: Optional[str] = None) -> Optional[str]:
        """
        Analyze a single topic using Gemini API
        
        Args:
            topic (str): The topic to analyze
            custom_prompt (str, optional): Custom prompt template. If None, uses default.
        
        Returns:
            str: Analysis result or None if failed
        """
        if not custom_prompt:
            custom_prompt = f"Analyze this trending Reddit topic and explain why it might be popular: {topic}"
        else:
            custom_prompt = custom_prompt.format(topic=topic)
        
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": custom_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "stopSequences": ["Title"],
                "temperature": 1.0,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error analyzing '{topic}': {e}")
            return None
    
    def analyze_topics(self, topics: List[str], custom_prompt: Optional[str] = None) -> dict:
        """
        Analyze multiple topics using Gemini API
        
        Args:
            topics (List[str]): List of topics to analyze
            custom_prompt (str, optional): Custom prompt template with {topic} placeholder
        
        Returns:
            dict: Dictionary with topic as key and analysis as value
        """
        results = {}
        
        print("\n🤖 AI Analysis of Trending Topics:\n")
        
        for topic in topics:
            print(f"📊 Analyzing '{topic}'...")
            analysis = self.analyze_topic(topic, custom_prompt)
            
            if analysis:
                print(f"📊 Analysis for '{topic}':")
                print(f"{analysis}\n")
                print("-" * 60)
                results[topic] = analysis
            else:
                print(f"❌ No analysis available for '{topic}'\n")
                results[topic] = None
        
        return results
    
    def generate_content(self, prompt: str, **config_overrides) -> Optional[str]:
        """
        Generate content using Gemini API with custom configuration
        
        Args:
            prompt (str): The prompt to send to Gemini
            **config_overrides: Override default generation config
        
        Returns:
            str: Generated content or None if failed
        """
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Default generation config
        generation_config = {
            "stopSequences": ["Title"],
            "temperature": 1.0,
            "topP": 0.8,
            "topK": 10
        }
        
        # Apply any overrides
        generation_config.update(config_overrides)
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": generation_config
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error generating content: {e}")
            return None

# Example usage
if __name__ == "__main__":
    try:
        gemini = GeminiAPI()
        
        # Test single topic analysis
        test_topic = "Artificial Intelligence"
        result = gemini.analyze_topic(test_topic)
        
        if result:
            print(f"Analysis for '{test_topic}':")
            print(result)
        else:
            print("Failed to get analysis")
            
    except ValueError as e:
        print(f"❌ {e}")
        print("Please add GEMINI_API_KEY to your .env file")
