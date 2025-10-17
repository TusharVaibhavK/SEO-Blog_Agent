import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.optimized_engine import seo_agent

def test_optimized_engine():
    print("🧪 Testing Optimized Free Tier SEO Agent...")
    
    # Test with a simple keyword
    seed = "digital marketing"
    
    try:
        df = seo_agent.analyze_keywords(seed, 10)
        print(f"✅ Success! Generated {len(df)} keywords")
        print("\nTop 5 keywords:")
        for i, row in df.head().iterrows():
            print(f"  {i+1}. {row['keyword']} (Vol: {row['estimated_volume']}, Comp: {row['competition_score']:.3f})")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_optimized_engine()
