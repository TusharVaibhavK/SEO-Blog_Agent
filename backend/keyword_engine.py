# import os
# import re
# import pandas as pd
# from typing import List, Dict, Tuple
# from dotenv import load_dotenv
# import openai
# import requests
# import json
# from collections import Counter

# load_dotenv()

# class SEOKeywordAgent:
#     def __init__(self):
#         # Initialize OpenAI with compatible syntax
#         openai.api_key = os.getenv('OPENAI_API_KEY')
#         self.serpapi_key = os.getenv('SERPAPI_API_KEY')
        
#     def expand_keywords_llm(self, seed_keyword: str, num_candidates: int = 200) -> List[str]:
#         """Use LLM to generate keyword variations"""
        
#         prompt = f"""
#         As an SEO expert, generate {num_candidates} diverse keyword variations for: "{seed_keyword}"
        
#         Include:
#         - Long-tail keywords (3+ words)
#         - Question-based keywords
#         - Location-based variations
#         - "How to" and tutorial style
#         - Comparison keywords
#         - Buyer intent keywords
#         - Informational intent keywords
        
#         Return ONLY a JSON array of strings, no explanations:
#         ["keyword1", "keyword2", ...]
#         """
        
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are an SEO expert specializing in keyword research. Always return valid JSON arrays."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=2000
#             )
            
#             keywords_text = response.choices[0].message.content.strip()
#             # Clean the response and parse JSON
#             keywords_text = re.sub(r'^```json\s*|\s*```$', '', keywords_text)
#             keywords = json.loads(keywords_text)
            
#             return keywords[:num_candidates]
            
#         except Exception as e:
#             print(f"LLM expansion failed: {e}")
#             print("Using fallback keyword expansion...")
#             # Fallback: basic keyword variations
#             return self._fallback_keyword_expansion(seed_keyword)
    
#     def _fallback_keyword_expansion(self, seed_keyword: str) -> List[str]:
#         """Fallback keyword expansion if LLM fails"""
#         base_words = seed_keyword.split()
#         modifiers = [
#             'best', 'top', 'review', 'guide', 'how to', 'what is', 
#             'vs', 'comparison', 'buy', 'price', 'cost', 'free',
#             '2024', '2025', 'near me', 'online', 'cheap', 'professional'
#         ]
        
#         variations = [seed_keyword]
#         for modifier in modifiers:
#             variations.append(f"{modifier} {seed_keyword}")
#             variations.append(f"{seed_keyword} {modifier}")
        
#         # Ensure we return enough variations
#         while len(variations) < 50:
#             for mod1 in modifiers:
#                 for mod2 in modifiers:
#                     if mod1 != mod2:
#                         variations.append(f"{mod1} {seed_keyword} {mod2}")
#                         if len(variations) >= 100:
#                             return variations[:100]
        
#         return variations[:100]
    
#     def deduplicate_keywords(self, keywords: List[str]) -> List[str]:
#         """Remove duplicates and normalize keywords"""
#         seen = set()
#         unique_keywords = []
        
#         for keyword in keywords:
#             # Normalize: lowercase, remove extra spaces
#             normalized = ' '.join(keyword.lower().split())
#             if normalized not in seen and len(normalized) > 2:
#                 seen.add(normalized)
#                 unique_keywords.append(keyword)
        
#         return unique_keywords
    
#     def get_serp_metrics(self, keyword: str) -> Dict:
#         """Get SERP metrics using SerpApi (fallback to simulated data)"""
        
#         if self.serpapi_key and self.serpapi_key != 'your_serpapi_key_here':
#             try:
#                 params = {
#                     'engine': 'google',
#                     'q': keyword,
#                     'api_key': self.serpapi_key,
#                     'num': 10
#                 }
                
#                 response = requests.get('https://serpapi.com/search', params=params)
#                 if response.status_code == 200:
#                     data = response.json()
#                     return self._analyze_serp_data(data, keyword)
                    
#             except Exception as e:
#                 print(f"SerpApi failed for '{keyword}': {e}")
        
#         # Fallback: simulated metrics
#         return self._simulate_metrics(keyword)
    
#     def _analyze_serp_data(self, serp_data: Dict, keyword: str) -> Dict:
#         """Analyze SERP data to estimate competition"""
#         organic_results = serp_data.get('organic_results', [])
        
#         # Simple competition heuristic based on top domains
#         strong_domains = ['wikipedia.org', 'amazon.com', 'youtube.com', 'forbes.com']
#         domain_count = Counter()
#         total_results = int(serp_data.get('search_information', {}).get('total_results', 1000000))
        
#         for result in organic_results[:10]:
#             domain = result.get('link', '').split('/')[2] if '/' in result.get('link', '') else ''
#             domain_count[domain] += 1
        
#         # Competition score (0-1, higher = more competitive)
#         strong_domain_presence = sum(1 for domain in domain_count if any(sd in domain for sd in strong_domains))
#         competition_score = min(1.0, (strong_domain_presence / 5) + (len(organic_results) / 20))
        
#         # Simulated volume based on keyword characteristics
#         word_count = len(keyword.split())
#         volume = max(100, 5000 - (word_count * 800))  # Basic inverse relationship
        
#         return {
#             'keyword': keyword,
#             'estimated_volume': volume,
#             'competition_score': round(competition_score, 3),
#             'serp_results_count': total_results,
#             'strong_domains_count': strong_domain_presence,
#             'top_domains': list(domain_count.keys())[:3]
#         }
    
#     def _simulate_metrics(self, keyword: str) -> Dict:
#         """Generate simulated metrics when APIs are unavailable"""
#         word_count = len(keyword.split())
        
#         # Simulate volume (long-tail = lower volume)
#         base_volume = 5000
#         volume_penalty = word_count * 600
#         volume = max(100, base_volume - volume_penalty)
        
#         # Simulate competition (long-tail = lower competition)
#         base_competition = 0.7
#         competition_bonus = word_count * 0.1
#         competition_score = min(0.95, max(0.1, base_competition - competition_bonus))
        
#         return {
#             'keyword': keyword,
#             'estimated_volume': volume,
#             'competition_score': round(competition_score, 3),
#             'serp_results_count': 1000000,
#             'strong_domains_count': 3,
#             'top_domains': ['example.com', 'sample.org', 'test.net'],
#             'note': 'simulated_data'
#         }
    
#     def calculate_composite_score(self, volume: int, competition: float, alpha: float = 0.6, beta: float = 0.4) -> float:
#         """
#         Calculate composite score for ranking
#         score = α*(normalized_volume) - β*(competition_score)
#         Higher score = better opportunity
#         """
#         # Normalize volume (assuming max ~5000)
#         normalized_volume = min(volume / 5000, 1.0)
        
#         composite_score = (alpha * normalized_volume) - (beta * competition)
#         return round(composite_score, 4)
    
#     def analyze_keywords(self, seed_keyword: str, top_n: int = 50) -> pd.DataFrame:
#         """Main analysis pipeline"""
#         print(f"🔍 Expanding keywords for: {seed_keyword}")
        
#         # Step 1: Generate keyword variations
#         raw_keywords = self.expand_keywords_llm(seed_keyword, 100)  # Reduced for speed
#         unique_keywords = self.deduplicate_keywords(raw_keywords)
        
#         print(f"📊 Generated {len(unique_keywords)} unique keywords")
        
#         # Step 2: Get metrics for each keyword
#         keyword_metrics = []
#         for i, keyword in enumerate(unique_keywords[:50]):  # Limit to first 50 for speed
#             print(f"   Analyzing {i+1}/{min(50, len(unique_keywords))}: {keyword}")
#             metrics = self.get_serp_metrics(keyword)
#             keyword_metrics.append(metrics)
        
#         # Step 3: Calculate scores and sort
#         for metrics in keyword_metrics:
#             metrics['composite_score'] = self.calculate_composite_score(
#                 metrics['estimated_volume'], 
#                 metrics['competition_score']
#             )
        
#         # Sort by composite score (highest opportunity first)
#         sorted_metrics = sorted(keyword_metrics, key=lambda x: x['composite_score'], reverse=True)
        
#         # Convert to DataFrame
#         df = pd.DataFrame(sorted_metrics[:top_n])
        
#         return df

# # Singleton instance
# keyword_agent = SEOKeywordAgent()

