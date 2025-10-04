#!/usr/bin/env python3
"""
Quick installation script for RAG dependencies
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Cerebras Chat Interface - RAG Installation Script       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    steps = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install python-dotenv", "Installing python-dotenv"),
        ("pip install markitdown", "Installing MarkItDown (document parsing)"),
        ("pip install pillow", "Installing Pillow (image processing)"),
        ("pip install sentence-transformers", "Installing sentence-transformers (embeddings)"),
        ("pip install qdrant-client", "Installing Qdrant client (vector database)"),
        ("pip install numpy tqdm", "Installing utilities"),
    ]
    
    failed = []
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            failed.append(desc)
    
    print(f"\n{'='*60}")
    print("📊 Installation Summary")
    print(f"{'='*60}")
    
    if failed:
        print(f"\n❌ Failed installations ({len(failed)}):")
        for item in failed:
            print(f"   - {item}")
        print("\n⚠️  Some components failed to install. RAG features may not work.")
        print("   Try installing manually: pip install -r requirements.txt")
    else:
        print("\n✅ All RAG dependencies installed successfully!")
        
        print("\n📝 Next Steps:")
        print("   1. Configure .env file (copy from .env.example)")
        print("   2. Set CEREBRAS_API_KEY in .env")
        print("   3. Choose Qdrant mode:")
        print("      - In-memory: Set QDRANT_IN_MEMORY=true (default)")
        print("      - Server: Run 'docker run -p 6333:6333 qdrant/qdrant'")
        print("   4. Run: python app.py")
        print("   5. Open: http://localhost:5000")
        
        print("\n📚 Documentation:")
        print("   - RAG Setup: See RAG_SETUP.md")
        print("   - General: See README.md")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
