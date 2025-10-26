#!/usr/bin/env python3
"""
Helper script to install missing dependencies
"""

import subprocess
import sys
import importlib

def check_and_install(package, import_name=None, version=None):
    """Check if a package is installed, and install it if not"""
    if import_name is None:
        import_name = package.split('==')[0].split('>=')[0]
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {import_name} is already installed")
        return True
    except ImportError:
        print(f"⚠️  {import_name} not found, installing...")
        try:
            if version:
                install_cmd = [sys.executable, "-m", "pip", "install", f"{package}>={version}"]
            else:
                install_cmd = [sys.executable, "-m", "pip", "install", package]
            
            subprocess.check_call(install_cmd)
            print(f"✅ {import_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {import_name}: {e}")
            return False

def main():
    """Main function to install all dependencies"""
    print("=" * 60)
    print("Installing Cerebras Chat Interface Dependencies")
    print("=" * 60)
    
    # Core dependencies
    dependencies = [
        ("flask==3.0.0", "flask"),
        ("flask-cors==4.0.0", "flask_cors"),
        ("flask-limiter==3.5.0", "flask_limiter"),
        ("limits==3.6.0", "limits"),
        ("python-dotenv==1.0.0", "dotenv"),
        ("certifi>=2023.7.22", "certifi"),
        ("requests>=2.31.0", "requests"),
        ("numpy>=1.24.0", "numpy"),
        ("tqdm>=4.65.0", "tqdm"),
    ]
    
    # RAG dependencies
    rag_dependencies = [
        ("sentence-transformers>=2.2.0", "sentence_transformers"),
        ("torch>=2.0.0", "torch"),
        ("qdrant-client>=1.7.0", "qdrant_client"),
        ("markitdown==0.0.1a2", "markitdown"),
        ("pillow>=10.0.0", "PIL"),
        ("huggingface-hub>=0.16.4", "huggingface_hub"),
    ]
    
    # Web search dependencies
    web_search_dependencies = [
        ("exa-py>=1.0.0", "exa_py"),
    ]
    
    # Try to install cerebras-cloud-sdk
    try:
        importlib.import_module("cerebras.cloud.sdk")
        print("✅ cerebras-cloud-sdk is already installed")
    except ImportError:
        print("⚠️  cerebras-cloud-sdk not found")
        print("   Please install it manually with: pip install cerebras-cloud-sdk")
        print("   Or visit: https://pypi.org/project/cerebras-cloud-sdk/")
    
    # Install core dependencies
    print("\nInstalling core dependencies...")
    for package, import_name in dependencies:
        check_and_install(package, import_name)
    
    # Install RAG dependencies
    print("\nInstalling RAG dependencies...")
    for package, import_name in rag_dependencies:
        check_and_install(package, import_name)
    
    # Install web search dependencies
    print("\nInstalling web search dependencies...")
    for package, import_name in web_search_dependencies:
        check_and_install(package, import_name)
    
    print("\n" + "=" * 60)
    print("Dependency installation complete!")
    print("You can now run the application with: python app.py")
    print("Or use the start_server.bat script on Windows")
    print("=" * 60)

if __name__ == "__main__":
    main()
