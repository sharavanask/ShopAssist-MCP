import asyncio
from server.buy import main

if __name__ == "__main__":
    print("Starting Amazon Product Search Server...")
    asyncio.run(main()) 