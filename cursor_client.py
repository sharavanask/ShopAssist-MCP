from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import time

async def connect_with_retry(max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to MCP server (attempt {attempt + 1}/{max_retries})...")
            
            # Connect to the already running server
            server_params = StdioServerParameters(
                command="python",
                args=["-m", "server.buy"],
                env=None,
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    print("Successfully connected to MCP server!")
                    
                    while True:
                        # Get user input
                        product = input("\nEnter product to search (or 'quit' to exit): ")
                        if product.lower() == 'quit':
                            break
                            
                        features = input("Enter specific features (press Enter to skip): ")
                        min_price = float(input("Enter minimum price (press Enter for default 1): ") or "1")
                        max_price = float(input("Enter maximum price (press Enter for default 999999): ") or "999999")
                        
                        print("\nSearching for products...")
                        result = await session.call_tool(
                            "getdata",
                            arguments={
                                "prod": product,
                                "specific_features": features,
                                "minp": min_price,
                                "maxp": max_price
                            }
                        )
                        
                        print("\nSearch Results:")
                        print(result.content[0].text if result.content else "No results found")
                    
                    return
                    
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print("Failed to connect after all retry attempts.")
                raise

async def main():
    try:
        await connect_with_retry()
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure the MCP server is running in a separate terminal with:")
        print("uv run server/buy.py")

if __name__ == "__main__":
    asyncio.run(main()) 