import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_nvidia_qwen():
    api_key = os.getenv('NVIDIA_API_KEY')
    base_url = os.getenv('NVIDIA_BASE_URL')
    model = "qwen/qwen-2.5-72b-instruct"  # Let's try this model first
    
    print(f"🔧 Testing NVIDIA API with model: {model}")
    print(f"🔑 API Key: {api_key[:20]}...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': 'Generate 5 SEO keyword variations for "python tutorial". Return as JSON array.'
            }
        ],
        'temperature': 0.7,
        'max_tokens': 500,
        'stream': False
    }
    
    try:
        response = requests.post(
            f'{base_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ Success! Response: {content[:200]}...")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_nvidia_qwen()
