#!/usr/bin/env python3
import os
import sys

def main():
    """Launch the Streamlit app"""
    app_path = os.path.join(os.path.dirname(__file__), 'web', 'streamlit_app.py')
    
    if os.path.exists(app_path):
        print("🚀 Starting Callus SEO Keyword Agent...")
        print("📊 Open your browser to http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Launch Streamlit
        os.system(f"streamlit run {app_path}")
    else:
        print(f"❌ Error: App not found at {app_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()