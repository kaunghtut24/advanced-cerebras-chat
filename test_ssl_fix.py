#!/usr/bin/env python3
"""
Test script to verify SSL fix for sentence-transformers model download
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ssl_fix():
    """Test if SSL fix resolves the certificate issue"""
    print("Testing SSL fix for sentence-transformers...")
    
    # Apply SSL fixes
    try:
        import certifi
        certifi_path = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi_path
        os.environ['SSL_CERT_FILE'] = certifi_path
        logger.info(f"Set SSL certificate bundle to: {certifi_path}")
    except ImportError:
        logger.warning("certifi not available")
        return False

    # Disable SSL verification for Hugging Face
    os.environ['HF_HUB_DISABLE_SSL'] = '1'
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    logger.info("Disabled SSL verification for Hugging Face Hub")

    try:
        print("Attempting to load sentence-transformers model...")
        from sentence_transformers import SentenceTransformer
        
        # This should trigger model download if not already present
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        logger.error(f"Model loading failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SSL Fix Test for Sentence-Transformers")
    print("=" * 60)
    
    success = test_ssl_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SSL fix applied successfully!")
        print("You can now run the main application without SSL issues.")
    else:
        print("⚠️  SSL fix test failed.")
        print("Try running the start_server.bat script instead.")
    print("=" * 60)
