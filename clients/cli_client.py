#!/usr/bin/env python3
"""
CLI Client for Amazon Product Search MCP Server
Simple command-line interface for searching products.
"""
import traceback
import asyncio
import argparse
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def search_products(product, features="", min_price=1.0, max_price=999999.0):
    """Search for products using the MCP server."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run","--with","mcp","mcp","run","server/buy.py"],
        env=None,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"🔍 Searching for: {product}")
                if features:
                    print(f"📋 Features: {features}")
                print(f"💰 Price range: ₹{min_price} - ₹{max_price}")
                print("-" * 50)
                
                result = await session.call_tool(
                    "getdata",
                    arguments={
                        "prod": product,
                        "specific_features": features,
                        "minp": min_price,
                        "maxp": max_price
                    }
                )
                
                if result.content:
                    print("✨ Recommendation:")
                    print("=" * 60)
                    print(result.content[0].text)
                    print("=" * 60)
                else:
                    print("❌ No results found")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit()

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Amazon Product Search CLI Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_client.py laptop --features "8GB RAM, SSD" --min-price 30000 --max-price 80000
  python cli_client.py smartphone --features "good camera, 5G" --min-price 15000
  python cli_client.py "wireless headphones" --max-price 5000
        """
    )
    
    parser.add_argument("product", help="Product to search for")
    parser.add_argument("--features", "-f", default="", help="Specific features to look for")
    parser.add_argument("--min-price", "-min", type=float, default=1.0, help="Minimum price")
    parser.add_argument("--max-price", "-max", type=float, default=999999.0, help="Maximum price")
    
    args = parser.parse_args()
    
    print("🛒 Amazon Product Search CLI Client")
    print("=" * 40)
    
    asyncio.run(search_products(
        args.product,
        args.features,
        args.min_price,
        args.max_price
    ))

if __name__ == "__main__":
    main() 