"""
Perplexity API Python Demo
-------------------------
This script demonstrates how to use the Perplexity API for chat completions with real-time web search and citations.

Requirements:
- openai>=1.0.0
- python-dotenv (optional, for loading API key from .env)

Setup:
1. Get your API key from https://www.perplexity.ai/settings/api
2. Set it as an environment variable (recommended) or in a .env file:
   SONAR_API_KEY=your-api-key-here

Docs: https://docs.perplexity.ai/guides/chat-completions-guide
"""
import os
from openai import OpenAI
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("SONAR_API_KEY")
if not API_KEY:
    raise RuntimeError("SONAR_API_KEY not set. Add it to your environment or .env file.")

# Initialize OpenAI client for Perplexity
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai"
)

# Example chat completion request
response = client.chat.completions.create(
    model="sonar-pro",  # Use 'sonar-pro' for best factuality and citations
    messages=[
        {"role": "system", "content": "You are a helpful assistant that always cites sources."},
        {"role": "user", "content": "Summarize the key features of the Perplexity API and how to use it."}
    ],
    max_tokens=512,
    temperature=0.2,
    stream=False
)

print("\n--- Perplexity API Demo Response ---\n")
print(response.choices[0].message.content)

# Print citations if available
citations = getattr(response, 'citations', None)
if citations:
    print("\nCitations:")
    for i, url in enumerate(citations, 1):
        print(f"  {i}. {url}")

# Save response and citations to a Markdown file
md_path = "perplexity_api_response.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Perplexity API Demo Response\n\n")
    f.write(response.choices[0].message.content + "\n\n")
    if citations:
        f.write("## Citations\n")
        for i, url in enumerate(citations, 1):
            f.write(f"{i}. {url}\n")
print(f"\nResponse also saved to {md_path}")


def perplexity_deep_research(query=None):
    """
    Conduct deep research using Perplexity's sonar-deep-research model.
    
    Args:
        query (str, optional): Research query. If None, uses default quantum computing query.
    
    Returns:
        str: The research response content
    """
    if query is None:
        query = "Conduct a comprehensive analysis of the quantum computing industry, including technological approaches, key players, market opportunities, regulatory challenges, and commercial viability projections through 2035."
    
    response = client.chat.completions.create(
        model="sonar-deep-research",
        messages=[
            {"role": "user", "content": query}
        ],
        max_tokens=2048,  # Deep research typically needs more tokens
        temperature=0.1,  # Lower temperature for factual research
        stream=False
    )
    
    content = response.choices[0].message.content
    
    # Print the response
    print("\n--- Perplexity Deep Research Response ---\n")
    print(content)
    
    # Print citations if available
    citations = getattr(response, 'citations', None)
    if citations:
        print("\nCitations:")
        for i, url in enumerate(citations, 1):
            print(f"  {i}. {url}")
    
    return content

# Example usage:
result = perplexity_deep_research()
custom_result = perplexity_deep_research("Analyze the latest developments in AI safety research")
