#!/usr/bin/env python3
"""
Test script to verify environment variable loading and configuration
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("❌ python-dotenv not installed")
    sys.exit(1)
except Exception as e:
    print(f"❌ Could not load .env file: {e}")

def test_env_var(var_name, default_value=None, expected_type=str):
    """Test if an environment variable is properly loaded"""
    value = os.environ.get(var_name, default_value)
    
    if value is None:
        print(f"⚠️  {var_name}: Not set (optional)")
        return None
    
    try:
        if expected_type == int:
            value = int(value)
        elif expected_type == bool:
            value = value.lower() == 'true'
        
        print(f"✅ {var_name}: {value} ({type(value).__name__})")
        return value
    except ValueError:
        print(f"❌ {var_name}: Invalid value '{value}' for type {expected_type.__name__}")
        return None

def main():
    print("🔧 Testing Environment Variable Configuration")
    print("=" * 50)
    
    # Test required variables
    print("\n📋 Required Variables:")
    api_key = test_env_var('CEREBRAS_API_KEY')
    if api_key:
        print(f"   API Key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
    else:
        print("   ⚠️  No API key set - will run in mock mode")
    
    # Test optional configuration variables
    print("\n⚙️  Configuration Variables:")
    test_env_var('CEREBRAS_BASE_URL', 'https://api.cerebras.ai')
    test_env_var('FLASK_ENV', 'development')
    test_env_var('FLASK_DEBUG', 'False', bool)
    test_env_var('HOST', '0.0.0.0')
    test_env_var('PORT', '5000', int)
    test_env_var('LOG_LEVEL', 'INFO')
    
    print("\n🚀 Application Settings:")
    test_env_var('MAX_CONTENT_LENGTH', '16777216', int)
    test_env_var('MAX_HISTORY_LENGTH', '20', int)
    
    print("\n🛡️  Rate Limiting:")
    test_env_var('RATE_LIMIT_STORAGE', 'memory://')
    test_env_var('RATE_LIMIT_DEFAULT', '200 per day, 50 per hour')
    test_env_var('RATE_LIMIT_CHAT', '30 per minute')
    
    print("\n" + "=" * 50)
    print("✅ Environment variable test completed!")
    
    # Test if we can import the main app
    try:
        print("\n🧪 Testing application import...")
        import app
        print("✅ Application imports successfully")
        
        # Check if Cerebras client is available
        if hasattr(app, 'cerebras_available') and app.cerebras_available:
            print("✅ Cerebras SDK initialized and ready")
        else:
            print("⚠️  Cerebras SDK in mock mode (no API key)")
            
    except Exception as e:
        print(f"❌ Application import failed: {e}")

if __name__ == "__main__":
    main()
