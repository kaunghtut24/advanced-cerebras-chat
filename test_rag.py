#!/usr/bin/env python3
"""
Test script for RAG functionality
"""

import os
import sys
import requests
import json
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

BASE_URL = "http://localhost:5000"

def test_rag_status():
    """Test RAG service status"""
    print("\n🔍 Testing RAG Status...")
    try:
        response = requests.get(f"{BASE_URL}/rag/status")
        data = response.json()
        
        if data.get('available'):
            print("✅ RAG service is available")
            print(f"   Embedding model: {data.get('embedding_model')}")
            print(f"   In-memory mode: {data.get('in_memory')}")
            print(f"   Settings: {json.dumps(data.get('settings', {}), indent=2)}")
            return True
        else:
            print("❌ RAG service not available")
            print(f"   Message: {data.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_kb(kb_name="test_kb"):
    """Test creating a knowledge base"""
    print(f"\n📚 Creating knowledge base '{kb_name}'...")
    try:
        response = requests.post(
            f"{BASE_URL}/knowledge-bases",
            json={"name": kb_name}
        )
        
        if response.status_code == 200:
            print(f"✅ Knowledge base '{kb_name}' created")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_kbs():
    """Test listing knowledge bases"""
    print("\n📋 Listing knowledge bases...")
    try:
        response = requests.get(f"{BASE_URL}/knowledge-bases")
        kbs = response.json()
        
        if kbs:
            print(f"✅ Found {len(kbs)} knowledge base(s):")
            for kb in kbs:
                print(f"   - {kb['name']}: {kb['vectors_count']} chunks")
        else:
            print("⚠️  No knowledge bases found")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_upload_file(kb_name="test_kb"):
    """Test file upload"""
    print(f"\n📤 Testing file upload to '{kb_name}'...")
    
    # Create a test text file
    test_file_path = "test_document.txt"
    test_content = """
    This is a test document for RAG functionality.
    
    Cerebras is a company that builds AI accelerators.
    The Cerebras Wafer-Scale Engine is the largest chip ever built.
    It enables fast inference for large language models.
    
    RAG (Retrieval-Augmented Generation) combines retrieval with generation.
    It helps AI models access external knowledge bases.
    This improves accuracy and reduces hallucinations.
    """
    
    try:
        # Write test file
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        # Upload file
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path, f, 'text/plain')}
            response = requests.post(
                f"{BASE_URL}/knowledge-bases/{kb_name}/upload",
                files=files
            )
        
        # Clean up
        os.remove(test_file_path)
        
        if response.status_code == 200:
            print(f"✅ File uploaded successfully")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        return False

def test_search(kb_name="test_kb", query="What is Cerebras?"):
    """Test searching in knowledge base"""
    print(f"\n🔎 Searching in '{kb_name}' for: '{query}'...")
    try:
        response = requests.post(
            f"{BASE_URL}/knowledge-bases/{kb_name}/search",
            json={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                print(f"✅ Found {len(results)} result(s):")
                for i, result in enumerate(results, 1):
                    print(f"\n   Result {i}:")
                    print(f"   Score: {result['score']:.3f}")
                    print(f"   File: {result['file_name']}")
                    print(f"   Text: {result['text'][:100]}...")
            else:
                print("⚠️  No results found")
            return True
        else:
            print(f"❌ Search failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_with_rag(kb_name="test_kb", message="What is Cerebras?"):
    """Test chat with RAG enabled"""
    print(f"\n💬 Testing chat with RAG...")
    try:
        # Create a session first
        session_response = requests.post(f"{BASE_URL}/sessions")
        session_id = session_response.json()['session_id']
        
        # Send chat message with RAG
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id,
                "use_rag": True,
                "kb_name": kb_name
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response received")
            print(f"   Response: {data['response'][:200]}...")
            
            if data.get('rag_sources'):
                print(f"   RAG Sources: {len(data['rag_sources'])} chunks used")
            else:
                print("   ⚠️  No RAG sources in response")
            return True
        else:
            print(f"❌ Chat failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        Cerebras Chat Interface - RAG Test Suite          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"Testing against: {BASE_URL}")
    print("Make sure the application is running (python app.py)")
    
    input("\nPress Enter to start tests...")
    
    # Run tests
    tests = [
        ("RAG Status", lambda: test_rag_status()),
        ("Create KB", lambda: test_create_kb()),
        ("List KBs", lambda: test_list_kbs()),
        ("Upload File", lambda: test_upload_file()),
        ("Search KB", lambda: test_search()),
        ("Chat with RAG", lambda: test_chat_with_rag()),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! RAG system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
