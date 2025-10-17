import os
import requests
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class NIMClient:
    def __init__(self):
        self.api_key = os.getenv('NVIDIA_API_KEY')
        self.base_url = os.getenv('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1')
        self.model = os.getenv('NVIDIA_MODEL', 'meta/llama-3-70b-instruct')
        
    def generate_keywords(self, seed_keyword: str, num_candidates: int = 100) -> List[str]:
        """Generate keyword variations using NVIDIA NIM"""
        
        prompt = f"""As an SEO expert, generate {num_candidates} diverse keyword variations for: "{seed_keyword}"

Include:
- Long-tail keywords (3+ words)
- Question-based keywords  
- Location-based variations
- "How to" and tutorial style
- Comparison keywords
- Buyer intent keywords
- Informational intent keywords

Return ONLY a JSON array of strings, no explanations:
["keyword1", "keyword2", ...]"""
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an SEO expert. Always return valid JSON arrays without explanations.'
                    },
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 2000,
                'stream': False
            }
            
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                keywords_text = result['choices'][0]['message']['content'].strip()
                
                # Clean and parse JSON
                import re
                keywords_text = re.sub(r'^```json\s*|\s*```$', '', keywords_text)
                keywords = json.loads(keywords_text)
                
                return keywords[:num_candidates]
            else:
                print(f"NVIDIA API Error: {response.status_code} - {response.text}")
                return self._fallback_expansion(seed_keyword)
                
        except Exception as e:
            print(f"NVIDIA NIM request failed: {e}")
            return self._fallback_expansion(seed_keyword)
    
    def _fallback_expansion(self, seed_keyword: str) -> List[str]:
        """Fallback keyword expansion"""
        base_words = seed_keyword.split()
        modifiers = [
            'best', 'top', 'review', 'guide', 'how to', 'what is', 
            'vs', 'comparison', 'buy', 'price', 'cost', 'free',
            '2024', '2025', 'near me', 'online', 'cheap', 'professional'
        ]
        
        variations = [seed_keyword]
        for modifier in modifiers:
            variations.append(f"{modifier} {seed_keyword}")
            variations.append(f"{seed_keyword} {modifier}")
        
        # Generate more combinations
        for mod1 in modifiers:
            for mod2 in modifiers:
                if mod1 != mod2 and len(variations) < 100:
                    variations.append(f"{mod1} {seed_keyword} {mod2}")
        
        return variations[:100]

# Test the client
if __name__ == "__main__":
    client = NIMClient()
    test_keywords = client.generate_keywords("python tutorial", 10)
    print(f"Generated {len(test_keywords)} keywords:")
    for kw in test_keywords[:5]:
        print(f"  - {kw}")
