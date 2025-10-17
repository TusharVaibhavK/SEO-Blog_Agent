# import streamlit as st
# import pandas as pd
# import sys
# import os
# from datetime import datetime

# # Add backend to path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from backend.keyword_engine import SEOKeywordAgent

# # Page configuration
# st.set_page_config(
#     page_title="Callus SEO Keyword Agent",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .success-box {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         color: #155724;
#     }
#     .metric-card {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #1f77b4;
#         margin: 0.5rem 0;
#     }
#     .keyword-table {
#         font-size: 0.9rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# def main():
#     # Header
#     st.markdown('<h1 class="main-header">🔍 Callus SEO Keyword Research Agent</h1>', unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Configuration")
        
#         st.subheader("API Settings")
#         openai_key = st.text_input("OpenAI API Key (optional)", type="password", 
#                                  help="Leave empty to use fallback keyword expansion")
#         serpapi_key = st.text_input("SerpApi Key (optional)", type="password",
#                                   help="Leave empty to use simulated metrics")
        
#         st.subheader("Analysis Parameters")
#         num_keywords = st.slider("Number of keywords to analyze", 10, 100, 50)
#         alpha = st.slider("Volume weight (α)", 0.1, 0.9, 0.6, 
#                          help="Higher values prioritize search volume")
#         beta = st.slider("Competition weight (β)", 0.1, 0.9, 0.4,
#                         help="Higher values penalize competition more")
        
#         st.markdown("---")
#         st.info("**Scoring Formula:**\n\n`score = α × volume - β × competition`\n\nHigher scores = Better opportunities")
    
#     # Main content area
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("🎯 Enter Seed Keyword")
#         seed_keyword = st.text_input(
#             "What topic would you like to research?",
#             placeholder="e.g., python tutorial, digital marketing, healthy recipes...",
#             help="Enter a broad topic to generate targeted keyword ideas"
#         )
        
#         analyze_button = st.button("🚀 Analyze Keywords", type="primary", use_container_width=True)
    
#     with col2:
#         st.subheader("📊 How It Works")
#         st.markdown("""
#         1. **Expand** - Generate 100+ keyword variations
#         2. **Analyze** - Estimate volume & competition  
#         3. **Score** - Rank by opportunity score
#         4. **Recommend** - Show top 50 low-competition, high-volume keywords
#         """)
        
#         st.markdown("---")
#         st.caption("⏰ Analysis takes 1-2 minutes")
    
#     # Analysis section
#     if analyze_button and seed_keyword:
#         if not seed_keyword.strip():
#             st.error("⚠️ Please enter a valid seed keyword")
#             return
        
#         # Update API keys if provided
#         agent = SEOKeywordAgent()
#         if openai_key:
#             import openai
#             openai.api_key = openai_key
        
#         if serpapi_key:
#             agent.serpapi_key = serpapi_key
        
#         # Show progress
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         with st.spinner("🔍 Starting keyword analysis..."):
#             # Update scoring parameters
#             agent.calculate_composite_score = lambda volume, competition: (
#                 alpha * min(volume / 5000, 1.0) - beta * competition
#             )
            
#             # Run analysis
#             status_text.text("🔄 Generating keyword variations...")
#             progress_bar.progress(20)
            
#             df = agent.analyze_keywords(seed_keyword, num_keywords)
            
#             status_text.text("📊 Calculating metrics and scores...")
#             progress_bar.progress(70)
            
#             status_text.text("🎯 Ranking opportunities...")
#             progress_bar.progress(90)
        
#         progress_bar.progress(100)
#         status_text.text("✅ Analysis complete!")
        
#         # Display results
#         st.markdown("---")
#         st.subheader("📈 Analysis Results")
        
#         # Summary metrics
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             avg_volume = df['estimated_volume'].mean()
#             st.metric("Average Monthly Volume", f"{avg_volume:,.0f}")
        
#         with col2:
#             avg_competition = df['competition_score'].mean()
#             st.metric("Average Competition", f"{avg_competition:.2f}")
        
#         with col3:
#             best_score = df['composite_score'].max()
#             st.metric("Best Opportunity Score", f"{best_score:.3f}")
        
#         with col4:
#             long_tail_pct = len(df[df['keyword'].str.split().str.len() >= 3]) / len(df) * 100
#             st.metric("Long-tail Keywords", f"{long_tail_pct:.1f}%")
        
#         # Results table
#         st.subheader(f"🎯 Top {len(df)} Keyword Opportunities")
        
#         # Format the dataframe for display
#         display_df = df.copy()
#         display_df['estimated_volume'] = display_df['estimated_volume'].astype(int)
#         display_df['competition_score'] = display_df['competition_score'].round(3)
#         display_df['composite_score'] = display_df['composite_score'].round(4)
        
#         # Add ranking
#         display_df['Rank'] = range(1, len(display_df) + 1)
#         display_df = display_df[['Rank', 'keyword', 'estimated_volume', 'competition_score', 'composite_score']]
#         display_df.columns = ['Rank', 'Keyword', 'Monthly Volume', 'Competition', 'Opportunity Score']
        
#         # Display table
#         st.dataframe(
#             display_df,
#             use_container_width=True,
#             height=600
#         )
        
#         # Export options
#         st.subheader("📤 Export Results")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # CSV download
#             csv = df.to_csv(index=False)
#             st.download_button(
#                 label="📥 Download CSV",
#                 data=csv,
#                 file_name=f"seo_keywords_{seed_keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
#                 mime="text/csv",
#                 use_container_width=True
#             )
        
#         with col2:
#             # Show raw data
#             if st.button("🔍 View Raw Data", use_container_width=True):
#                 st.json(df.to_dict(orient='records'))
        
#         # Top recommendations
#         st.subheader("🏆 Top 5 Recommendations")
#         top_5 = df.head(5)
        
#         for i, (_, row) in enumerate(top_5.iterrows(), 1):
#             with st.container():
#                 col1, col2, col3 = st.columns([3, 1, 1])
                
#                 with col1:
#                     st.markdown(f"**{i}. {row['keyword']}**")
                
#                 with col2:
#                     st.metric("Volume", f"{row['estimated_volume']:,.0f}")
                
#                 with col3:
#                     st.metric("Competition", f"{row['competition_score']:.2f}")
                
#                 st.markdown("---")
        
#         # Data source info
#         with st.expander("ℹ️ About the Data"):
#             st.markdown("""
#             **Data Sources & Methods:**
            
#             - **Keyword Expansion**: OpenAI GPT-3.5-turbo (with fallback to rule-based generation)
#             - **Search Volume**: Estimated based on keyword characteristics and length
#             - **Competition Score**: Based on SERP analysis (0-1 scale, lower is better)
#             - **Opportunity Score**: Custom formula balancing volume and competition
            
#             **Note**: For production use, integrate with:
#             - Google Ads Keyword Planner API (accurate volumes)
#             - SerpApi (real SERP data)
#             - SEMrush/Ahrefs APIs (competition metrics)
#             """)
    
#     elif analyze_button and not seed_keyword:
#         st.error("⚠️ Please enter a seed keyword to analyze")

# if __name__ == "__main__":
#     main()

## Testing new Streamlit app code with optimizations
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.optimized_engine import seo_agent
    ENGINE_TYPE = "🚀 Optimized Free Tier Engine"
except ImportError:
    from backend.keyword_engine import keyword_agent as seo_agent
    ENGINE_TYPE = "🔧 Basic Engine"

# Page configuration
st.set_page_config(
    page_title="Callus SEO Keyword Agent - Free Tier",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .engine-badge {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .free-tier-badge {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with engine info
    st.markdown('<h1 class="main-header">🔍 Callus SEO Keyword Research Agent</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="engine-badge">{ENGINE_TYPE} <span class="free-tier-badge">FREE TIER OPTIMIZED</span></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Free Tier Configuration")
        
        st.subheader("🔑 API Status")
        nvidia_status = "✅ Connected" if os.getenv('NVIDIA_API_KEY') else "❌ Not Set"
        serpapi_status = "✅ Connected" if os.getenv('SERPAPI_API_KEY') else "❌ Not Set"
        
        st.write(f"NVIDIA NIM: {nvidia_status}")
        st.write(f"SerpApi: {serpapi_status}")
        
        st.subheader("🎯 Analysis Parameters")
        num_keywords = st.slider("Keywords to analyze", 10, 50, 25, 
                               help="Free tier optimized: Lower = faster, more reliable")
        
        alpha = st.slider("Volume weight (α)", 0.1, 0.9, 0.6,
                         help="How much to prioritize search volume")
        beta = st.slider("Competition weight (β)", 0.1, 0.9, 0.4,
                        help="How much to penalize high competition")
        
        st.markdown("---")
        st.info("""
        **Free Tier Optimizations:**
        - Smart caching
        - Rate limiting
        - Enhanced fallbacks
        - Realistic simulations
        """)
        
        st.warning("""
        **Free Tier Limits:**
        - NVIDIA: ~5 requests/min
        - SerpApi: 100 searches/month
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Enter Seed Keyword")
        seed_keyword = st.text_input(
            "What topic would you like to research?",
            placeholder="e.g., python tutorial, healthy recipes, digital marketing...",
            help="Keep it broad for best results"
        )
        
        analyze_clicked = st.button("🚀 Analyze Keywords (Free Tier Optimized)", 
                                  type="primary", 
                                  use_container_width=True)
    
    with col2:
        st.subheader("💡 Free Tier Tips")
        st.markdown("""
        - **Start broad**: "python" vs "python web scraping"
        - **Use common terms**: Higher quality simulations
        - **Be patient**: Free APIs have rate limits
        - **Export results**: Save your analysis
        """)
        
        st.markdown("---")
        st.caption("⏱️ Analysis: 1-3 minutes (free tier optimized)")
    
    # Analysis
    if analyze_clicked and seed_keyword:
        if not seed_keyword.strip():
            st.error("⚠️ Please enter a valid seed keyword")
            return
        
        # Analysis progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_placeholder = st.empty()
        
        try:
            # Update scoring function
            def custom_scorer(volume, competition):
                norm_volume = min(volume / 5000, 1.0)
                return (alpha * norm_volume) - (beta * competition)
            
            # Run analysis
            status_text.text("🔄 Generating keyword variations with NVIDIA Qwen...")
            progress_bar.progress(20)
            
            # Small delay to simulate processing
            import time
            time.sleep(1)
            
            status_text.text("📊 Analyzing competition and volumes...")
            progress_bar.progress(50)
            
            # Perform analysis
            df = seo_agent.analyze_keywords(seed_keyword, num_keywords)
            
            status_text.text("🎯 Ranking opportunities...")
            progress_bar.progress(80)
            
            # Apply custom scoring
            df['composite_score'] = df.apply(
                lambda row: custom_scorer(row['estimated_volume'], row['competition_score']), 
                axis=1
            )
            df = df.sort_values('composite_score', ascending=False)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Display results
            display_results(df, seed_keyword)
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("💡 Try a different keyword or check your API keys")
    
    elif analyze_clicked and not seed_keyword:
        st.error("⚠️ Please enter a seed keyword to analyze")
    
    # Footer
    st.markdown("---")
    st.caption("🔧 Built with NVIDIA NIM Qwen • SerpApi • Streamlit • Free Tier Optimized")

def display_results(df, seed_keyword):
    """Display analysis results"""
    st.markdown("---")
    st.subheader("📈 Analysis Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_volume = df['estimated_volume'].mean()
        st.metric("Avg Monthly Volume", f"{avg_volume:,.0f}")
    
    with col2:
        avg_competition = df['competition_score'].mean()
        st.metric("Avg Competition", f"{avg_competition:.2f}")
    
    with col3:
        best_score = df['composite_score'].max()
        st.metric("Best Opportunity", f"{best_score:.3f}")
    
    with col4:
        long_tail = len(df[df['keyword'].str.split().str.len() >= 3])
        st.metric("Long-tail Keywords", f"{long_tail}/{len(df)}")
    
    # Results table
    st.subheader(f"🎯 Top {len(df)} Keyword Opportunities")
    
    display_df = df.copy()
    display_df['Rank'] = range(1, len(df) + 1)
    display_df = display_df[['Rank', 'keyword', 'estimated_volume', 'competition_score', 'composite_score', 'data_source']]
    display_df.columns = ['Rank', 'Keyword', 'Volume', 'Competition', 'Opportunity', 'Source']
    
    # Format numbers
    display_df['Volume'] = display_df['Volume'].astype(int)
    display_df['Competition'] = display_df['Competition'].round(3)
    display_df['Opportunity'] = display_df['Opportunity'].round(4)
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Export
    st.subheader("📤 Export Results")
    csv = df.to_csv(index=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"seo_keywords_{seed_keyword.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔍 View Data Sources", use_container_width=True):
            sources = df['data_source'].value_counts()
            st.write("Data sources used:")
            for source, count in sources.items():
                st.write(f"- {source}: {count} keywords")
    
    # Recommendations
    st.subheader("🏆 Top Recommendations")
    top_3 = df.head(3)
    
    for i, (_, row) in enumerate(top_3.iterrows(), 1):
        with st.container():
            cols = st.columns([3, 1, 1, 1])
            with cols[0]:
                st.write(f"**{i}. {row['keyword']}**")
            with cols[1]:
                st.metric("Volume", f"{row['estimated_volume']:,}")
            with cols[2]:
                st.metric("Competition", f"{row['competition_score']:.2f}")
            with cols[3]:
                st.metric("Score", f"{row['composite_score']:.3f}")

if __name__ == "__main__":
    main()