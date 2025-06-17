#!/usr/bin/env python3
"""
MCP Client for Amazon Product Search Server
This client demonstrates how to connect to and interact with your MCP server.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    """Main client function to interact with the MCP server."""
    
    # Server parameters - adjust the command to match your server setup
    server_params = StdioServerParameters(
        command="python",
        args=["../main.py"],  # Path to the main server file
        env=None,
    )
    
    print("🚀 Starting MCP Client...")
    print("Connecting to Amazon Product Search Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("✅ Connected to MCP server!")
            
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            print("\n📋 Available tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Example 1: Search for laptops
            print("\n🔍 Example 1: Searching for laptops...")
            try:
                result = await session.call_tool(
                    "getdata",
                    arguments={
                        "prod": "laptop",
                        "specific_features": "8GB RAM, SSD storage, good for programming",
                        "minp": 30000,
                        "maxp": 80000
                    }
                )
                print("Recommendation:")
                print(result.content[0].text if result.content else "No result")
            except Exception as e:
                print(f"Error: {e}")
            
            # Example 2: Search for smartphones
            print("\n📱 Example 2: Searching for smartphones...")
            try:
                result = await session.call_tool(
                    "getdata",
                    arguments={
                        "prod": "smartphone",
                        "specific_features": "good camera, long battery life, 5G support",
                        "minp": 15000,
                        "maxp": 50000
                    }
                )
                print("Recommendation:")
                print(result.content[0].text if result.content else "No result")
            except Exception as e:
                print(f"Error: {e}")
            
            # Interactive mode
            print("\n🎯 Interactive Mode (type 'exit' to quit):")
            while True:
                try:
                    product = input("\nEnter product to search for: ").strip()
                    if product.lower() == 'exit':
                        break
                    
                    features = input("Enter specific features (optional): ").strip()
                    
                    min_price = input("Enter minimum price (default 1): ").strip()
                    min_price = float(min_price) if min_price else 1.0
                    
                    max_price = input("Enter maximum price (default 999999): ").strip()
                    max_price = float(max_price) if max_price else 999999.0
                    
                    print(f"\n🔍 Searching for {product}...")
                    
                    result = await session.call_tool(
                        "getdata",
                        arguments={
                            "prod": product,
                            "specific_features": features,
                            "minp": min_price,
                            "maxp": max_price
                        }
                    )
                    
                    print("\n✨ Recommendation:")
                    print("=" * 50)
                    print(result.content[0].text if result.content else "No result")
                    print("=" * 50)
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_client()) 
    