"""
Test script to verify the Shopify app setup
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import requests
        print("✅ requests module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        from main import ShopifyAPI, Product
        print("✅ Main app modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import main app modules: {e}")
        return False
    
    return True

def test_env_file():
    """Check if .env file exists and has the required variables"""
    if os.path.exists('.env'):
        print("✅ .env file found")
        from dotenv import load_dotenv
        load_dotenv()
        
        shop_name = os.getenv('SHOPIFY_SHOP_NAME')
        access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        
        if shop_name and access_token:
            print("✅ Environment variables configured")
            return True
        else:
            print("⚠️  .env file exists but variables are not set")
            return False
    else:
        print("⚠️  .env file not found - you'll need to enter credentials manually")
        return False

def main():
    print("🧪 Testing Shopify App Setup")
    print("=" * 40)
    
    imports_ok = test_imports()
    env_ok = test_env_file()
    
    print("\n" + "=" * 40)
    if imports_ok:
        print("✅ Setup test passed! Your app is ready to use.")
        print("\nTo run the app: python main.py")
        if not env_ok:
            print("\n💡 Tip: Create a .env file with your credentials for easier usage")
            print("   See .env.example for the format")
    else:
        print("❌ Setup test failed! Please check the error messages above.")

if __name__ == "__main__":
    main()
