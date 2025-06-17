#!/usr/bin/env python3
"""
Web Client for Amazon Product Search MCP Server
This creates a REST API that interfaces with your MCP server.
"""
import os 
import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import uvicorn
import traceback

app = FastAPI(title="Amazon Product Search API", description="Web interface for MCP Amazon search server")

class ProductSearchRequest(BaseModel):
    product: str
    specific_features: str = ""
    min_price: float = 1.0
    max_price: float = 999999.0

class ProductSearchResponse(BaseModel):
    success: bool
    recommendation: str
    error: str = None

async def call_mcp_server(product: str, features: str, min_price: float, max_price: float):
    """Call the MCP server with the given parameters."""
    venv_python = os.path.abspath(".venv/Scripts/python.exe")  # For Windows
    # venv_python = os.path.abspath(".venv/bin/python")  # macOS/Linux

    buypy=os.path.abspath("serve/buy.py")
    print(f"🚀 Launching MCP using: {venv_python}")
    
    server_params = StdioServerParameters(
        command=venv_python,
        args=[buypy],  # Path to your MCP server
        env=None,
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ MCP session initialized. Calling tool 'getdata'...")
                await session.initialize()

                result = await session.call_tool(
                    "getdata",
                    arguments={
                        "prod": product,
                        "specific_features": features,
                        "minp": min_price,
                        "maxp": max_price
                    }
                )

                print("✅ Tool call successful.")
                return result.content[0].text if result.content else "No result"
    except Exception as e:
        print("❌ MCP Call failed with exception:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"MCP Error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve a simple HTML interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Amazon Product Search</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .result { margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 4px; background-color: #f9f9f9; }
            .loading { display: none; }
        </style>
    </head>
    <body>
        <h1>🛒 Amazon Product Search</h1>
        <form id="searchForm">
            <div class="form-group">
                <label for="product">Product:</label>
                <input type="text" id="product" name="product" required placeholder="e.g., laptop, smartphone, headphones">
            </div>
            <div class="form-group">
                <label for="features">Specific Features:</label>
                <textarea id="features" name="features" rows="3" placeholder="e.g., 8GB RAM, good camera, long battery life"></textarea>
            </div>
            <div class="form-group">
                <label for="minPrice">Minimum Price (₹):</label>
                <input type="number" id="minPrice" name="minPrice" value="1" min="1">
            </div>
            <div class="form-group">
                <label for="maxPrice">Maximum Price (₹):</label>
                <input type="number" id="maxPrice" name="maxPrice" value="999999" min="1">
            </div>
            <button type="submit">🔍 Search Products</button>
        </form>
        
        <div id="loading" class="loading">
            <p>🔄 Searching for products...</p>
        </div>
        
        <div id="result" class="result" style="display: none;">
            <h3>Recommendation:</h3>
            <pre id="recommendationText"></pre>
        </div>

        <script>
            document.getElementById('searchForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const loadingDiv = document.getElementById('loading');
                const resultDiv = document.getElementById('result');
                const recommendationText = document.getElementById('recommendationText');
                
                loadingDiv.style.display = 'block';
                resultDiv.style.display = 'none';
                
                const formData = new FormData(e.target);
                const data = {
                    product: formData.get('product'),
                    specific_features: formData.get('features'),
                    min_price: parseFloat(formData.get('minPrice')),
                    max_price: parseFloat(formData.get('maxPrice'))
                };
                
                try {
                    const response = await fetch('/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    loadingDiv.style.display = 'none';
                    
                    if (result.success) {
                        recommendationText.textContent = result.recommendation;
                        resultDiv.style.display = 'block';
                    } else {
                        alert('Error: ' + (result.error || 'Unknown error'));
                    }
                } catch (error) {
                    loadingDiv.style.display = 'none';
                    alert('Network error: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/search", response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    """Search for products using the MCP server."""
    try:
        recommendation = await call_mcp_server(
            request.product,
            request.specific_features,
            request.min_price,
            request.max_price
        )
        
        return ProductSearchResponse(
            success=True,
            recommendation=recommendation
        )
    except Exception as e:
        return ProductSearchResponse(
            success=False,
            recommendation="",
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Amazon Product Search API is running"}

if __name__ == "__main__":
    print("🌐 Starting Web Client for Amazon Product Search...")
    print("Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000) 