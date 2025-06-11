# Shopify Products Fetcher

A Python application to fetch and manage products from your Shopify store using the Shopify Admin API.

## Features

- Fetch products from your Shopify store
- Search products by title
- Display products in a formatted table
- Export products to JSON file
- Handle pagination for large product catalogs
- Secure credential management with environment variables

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Shopify Private App

1. Go to your Shopify admin panel
2. Navigate to **Apps** > **App and sales channel settings**
3. Click **Develop apps** > **Create an app**
4. Give your app a name (e.g., "Product Fetcher")
5. Click **Configure Admin API scopes**
6. Enable the following scopes:
   - `read_products` (required)
   - `read_inventory` (optional, for inventory data)
7. Click **Save** and then **Install app**
8. Copy the **Admin API access token**

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:

   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:

   ```
   SHOPIFY_SHOP_NAME=your-shop-name
   SHOPIFY_ACCESS_TOKEN=your-access-token
   ```

   **Note:** For `SHOPIFY_SHOP_NAME`, use only the shop name without `.myshopify.com`.
   For example, if your store URL is `mystore.myshopify.com`, use `mystore`.

## Usage

Run the application:

```bash
python main.py
```

### Menu Options

1. **Get first 50 products** - Quick preview of your products
2. **Get all products** - Fetch all products (uses pagination)
3. **Search products** - Search by product title
4. **Export products to JSON** - Save all products to a JSON file
5. **Exit** - Close the application

## Example Output

```
🛍️  Shopify Products Fetcher
==================================================

📋 Options:
1. Get first 50 products
2. Get all products
3. Search products
4. Export products to JSON
5. Exit

====================================================================================================
Found 25 products:
====================================================================================================
ID           Title                          Vendor          Type            Price      Status
----------------------------------------------------------------------------------------------------
123456789    Awesome T-Shirt                ACME Co         Apparel         $29.99     active
987654321    Cool Sneakers                  ShoeCorp        Footwear        $89.99     active
```

## API Rate Limits

The Shopify Admin API has rate limits:

- REST Admin API: 40 requests per app per store per minute
- The app handles pagination automatically to stay within limits

## Error Handling

The application includes comprehensive error handling for:

- Network connectivity issues
- Invalid credentials
- API rate limiting
- Missing products

## Security Notes

- Never commit your `.env` file to version control
- Keep your access token secure
- Regularly rotate your access tokens
- Only grant necessary permissions to your private app

## Troubleshooting

### Common Issues

1. **Authentication Error**: Verify your shop name and access token
2. **No Products Found**: Check if your store has products and the app has proper permissions
3. **Rate Limit Exceeded**: The app will handle this automatically, but you may need to wait

### Getting Help

If you encounter issues:

1. Check your Shopify app permissions
2. Verify your store URL and credentials
3. Ensure your products are published and active
