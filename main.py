import requests
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Product:
    """Data class for Shopify product"""
    id: int
    title: str
    handle: str
    vendor: str
    product_type: str
    status: str
    price: Optional[str] = None
    inventory_quantity: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create Product instance from Shopify API response"""
        price = None
        inventory_quantity = None
        
        if data.get('variants') and len(data['variants']) > 0:
            first_variant = data['variants'][0]
            price = first_variant.get('price')
            inventory_quantity = first_variant.get('inventory_quantity')
        
        return cls(
            id=data['id'],
            title=data['title'],
            handle=data['handle'],
            vendor=data['vendor'],
            product_type=data['product_type'],
            status=data['status'],
            price=price,
            inventory_quantity=inventory_quantity
        )

class ShopifyAPI:
    """Shopify API client for fetching products"""
    
    def __init__(self, shop_name: str, access_token: str):
        """
        Initialize Shopify API client
        
        Args:
            shop_name: Shopify store name (without .myshopify.com)
            access_token: Shopify private app access token
        """
        self.shop_name = shop_name
        self.access_token = access_token
        self.base_url = f"https://{shop_name}.myshopify.com"
        self.headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }
    
    def get_products(self, limit: int = 50, status: str = "active") -> List[Product]:
        """
        Fetch products from Shopify store
        
        Args:
            limit: Number of products to fetch (max 250)
            status: Product status filter ('active', 'archived', 'draft')
            
        Returns:
            List of Product objects
        """
        url = f"{self.base_url}/admin/api/2023-10/products.json"
        params = {
            "limit": min(limit, 250),
            "status": status
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            products_data = data.get('products', [])
            
            return [Product.from_dict(product) for product in products_data]
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            return []
    
    def get_all_products(self, status: str = "active") -> List[Product]:
        """
        Fetch all products using pagination
        
        Args:
            status: Product status filter
            
        Returns:
            List of all Product objects
        """
        all_products = []
        page_info = None
        
        while True:
            url = f"{self.base_url}/admin/api/2023-10/products.json"
            params = {
                "limit": 250,
                "status": status
            }
            
            if page_info:
                params["page_info"] = page_info
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                products_data = data.get('products', [])
                
                if not products_data:
                    break
                
                products = [Product.from_dict(product) for product in products_data]
                all_products.extend(products)
                
                # Check for pagination
                link_header = response.headers.get('Link')
                if link_header and 'rel="next"' in link_header:
                    # Extract page_info from Link header
                    for link in link_header.split(','):
                        if 'rel="next"' in link:
                            page_info = link.split('page_info=')[1].split('&')[0].split('>')[0]
                            break
                else:
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Error fetching products: {e}")
                break
        
        return all_products
    
    def search_products(self, query: str, limit: int = 50) -> List[Product]:
        """
        Search products by title, vendor, product type, or tag
        
        Args:
            query: Search query
            limit: Number of products to return
            
        Returns:
            List of matching Product objects
        """
        url = f"{self.base_url}/admin/api/2023-10/products.json"
        params = {
            "limit": min(limit, 250),
            "title": query
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            products_data = data.get('products', [])
            
            return [Product.from_dict(product) for product in products_data]
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching products: {e}")
            return []

def display_products(products: List[Product]):
    """Display products in a formatted table"""
    if not products:
        print("No products found.")
        return
    
    print(f"\n{'='*100}")
    print(f"Found {len(products)} products:")
    print(f"{'='*100}")
    print(f"{'ID':<12} {'Title':<30} {'Vendor':<15} {'Type':<15} {'Price':<10} {'Status':<10}")
    print(f"{'-'*100}")
    
    for product in products:
        title = product.title[:27] + "..." if len(product.title) > 30 else product.title
        vendor = product.vendor[:12] + "..." if len(product.vendor) > 15 else product.vendor
        product_type = product.product_type[:12] + "..." if len(product.product_type) > 15 else product.product_type
        price = f"${product.price}" if product.price else "N/A"
        
        print(f"{product.id:<12} {title:<30} {vendor:<15} {product_type:<15} {price:<10} {product.status:<10}")

def export_to_json(products: List[Product], filename: str = "shopify_products.json"):
    """Export products to JSON file"""
    products_dict = []
    for product in products:
        products_dict.append({
            "id": product.id,
            "title": product.title,
            "handle": product.handle,
            "vendor": product.vendor,
            "product_type": product.product_type,
            "status": product.status,
            "price": product.price,
            "inventory_quantity": product.inventory_quantity
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\nProducts exported to {filename}")

def main():
    """Main application function"""
    print("🛍️  Shopify Products Fetcher")
    print("=" * 50)
    
    # Get credentials from environment variables or user input
    shop_name = os.getenv('SHOPIFY_SHOP_NAME')
    access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    if not shop_name:
        shop_name = input("Enter your Shopify shop name (without .myshopify.com): ").strip()
    
    if not access_token:
        access_token = input("Enter your Shopify access token: ").strip()
    
    if not shop_name or not access_token:
        print("❌ Shop name and access token are required!")
        return
    
    # Initialize API client
    api = ShopifyAPI(shop_name, access_token)
    
    while True:
        print("\n📋 Options:")
        print("1. Get first 50 products")
        print("2. Get all products")
        print("3. Search products")
        print("4. Export products to JSON")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == "1":
            print("\n⏳ Fetching first 50 products...")
            products = api.get_products(limit=50)
            display_products(products)
            
        elif choice == "2":
            print("\n⏳ Fetching all products (this may take a while)...")
            products = api.get_all_products()
            display_products(products)
            
        elif choice == "3":
            query = input("Enter search term: ").strip()
            if query:
                print(f"\n⏳ Searching for products matching '{query}'...")
                products = api.search_products(query)
                display_products(products)
            else:
                print("❌ Please enter a search term!")
                
        elif choice == "4":
            print("\n⏳ Fetching all products for export...")
            products = api.get_all_products()
            if products:
                filename = input("Enter filename (default: shopify_products.json): ").strip()
                if not filename:
                    filename = "shopify_products.json"
                export_to_json(products, filename)
            else:
                print("❌ No products to export!")
                
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option! Please select 1-5.")

if __name__ == "__main__":
    main()