import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

# Supabase configuration
#get from env 
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
def test_supabase_connection():
  try:
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Alternative method if RPC doesn't work:
    # You can manually list your tables here
    table_names = ['products', 'store', 'sync_log']  # Replace with your actual table names
    
    print("✅ Connection successful!")
    
    # Query each table
    for table_name in table_names:
      try:
        response = supabase.table(table_name).select("*").execute()
        print(f"📊 Table '{table_name}': {len(response.data)} records")
        # Optionally print first few records
        if response.data:
          print(f"   Sample data: {response.data[:2]}")
      except Exception as table_error:
        print(f"❌ Error querying table '{table_name}': {table_error}")
    
    return True
    
  except Exception as e:
    print(f"❌ Connection failed: {e}")
    return False

if __name__ == "__main__":
  test_supabase_connection()