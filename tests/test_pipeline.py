#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.keyword_engine import SEOKeywordAgent

def test_basic_functionality():
    """Test the keyword engine with a sample seed"""
    agent = SEOKeywordAgent()
    
    # Test with a simple seed keyword
    seed = "python tutorial"
    
    print("🧪 Testing keyword expansion...")
    keywords = agent.expand_keywords_llm(seed, 10)
    print(f"Generated {len(keywords)} keywords:")
    for kw in keywords[:5]:
        print(f"  - {kw}")
    
    print("\n🧪 Testing deduplication...")
    unique = agent.deduplicate_keywords(keywords + keywords)  # Add duplicates
    print(f"Unique keywords: {len(unique)}")
    
    print("\n🧪 Testing metrics for one keyword...")
    metrics = agent.get_serp_metrics(keywords[0] if keywords else seed)
    print(f"Metrics for sample keyword:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    
    print("\n🧪 Testing composite score...")
    score = agent.calculate_composite_score(metrics['estimated_volume'], metrics['competition_score'])
    print(f"Composite score: {score}")
    
    print("\n✅ Basic functionality test completed!")
    return True

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("This might be due to missing API keys. The app will use simulated data.")