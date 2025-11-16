"""
Quick test to verify OpenAI API key is working
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('backend/.env')

# Check API key
api_key = os.getenv("OPENAI_API_KEY")

print("\n" + "="*60)
print("  🔑 API Key Test")
print("="*60)

if not api_key:
    print("\n❌ No API key found!")
    print("   Check backend/.env file")
elif api_key == "your_api_key_here":
    print("\n⚠️  API key is placeholder!")
    print("   Replace 'your_api_key_here' with your actual key")
else:
    print("\n✅ API key found!")
    print(f"   Key starts with: {api_key[:20]}...")
    print(f"   Key length: {len(api_key)} characters")
    
    # Test with OpenAI
    print("\n🧪 Testing OpenAI connection...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API key works!'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"   ✅ OpenAI responded: {result}")
        print("\n🎉 Your API key is working perfectly!")
        
    except Exception as e:
        print(f"   ❌ OpenAI error: {e}")
        print("\n   Possible issues:")
        print("   • API key is invalid")
        print("   • No credits/quota remaining")
        print("   • Network connection issue")

print("\n" + "="*60 + "\n")
