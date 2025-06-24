from typing import Any, Dict, List
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("amazonmcp")

HF_API_TOKEN="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"
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

print("decision_agent loaded")



### Option 1 Hugging face model 
async def decision_agent(top3_products_summary, user_input,specific_features):
    prompt = f"""
    You are an expert product advisor AI. Your job is to select the single best product for a Small or Medium Enterprise from the following Amazon product shortlist:

    {top3_products_summary}

    User requirements:
    - Product: {user_input}
    - Features: {specific_features}
    - Budget: Please consider the user's specified price range if available.

    Instructions:
    - Carefully match ALL required features and preferences with product specifications.
    - Prioritize products that meet all requirements and fall within the user needs.
    - Consider user needs: value for money, reliability, vendor reputation, and scalability.
    - If no product is a perfect match, pick the closest and clearly state any compromises.

    Output format:
    <Product Title>

    Justification: (5-8 lines explaining why this is the best choice, referencing features, price, and user fit)
    Pros: 3 lines
    Cons: 3 lines 
    """
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(HF_API_URL, headers=HEADERS, json=payload)
            res.raise_for_status()
    except httpx.HTTPStatusError as e:
        return e
    except httpx.RequestError as e:
        return e

    data = res.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        gen = data[0]["generated_text"]
        if gen.startswith(prompt):
            gen = gen[len(prompt):].strip()
        return gen.strip()
    else:
        return e

##Option 2 Groq developer API 

GROQ_API_KEY = "*****************************"  
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"  

async def decision_agent(top3_products_summary, user_input, specific_features):
    prompt = f"""
You are an expert product advisor AI. Your job is to select the single best product for a Small or Medium Enterprise from the following Amazon product shortlist:

{top3_products_summary}

User requirements:
- Product: {user_input}
- Features: {specific_features}
- Budget: Please consider the user's specified price range if available.

Instructions:
- Carefully match ALL required features and preferences with product specifications.
- Prioritize products that meet all requirements and fall within the user needs that has been specified above.
- Consider user needs: value for money, reliability, seller reputation, and service support of the brand too.
- If no product is a perfect match, pick the closest and clearly state any compromises.

Output format:
<Product Title>

Justification: (5-8 lines explaining why this is the best choice, referencing features, price, and user fit)
Pros: 3 lines
Cons: 3 lines
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(f"{GROQ_BASE_URL}/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"].strip()
    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Request Error: {str(e)}"


    

def summarize_product(product):
    return (
        f"Product: {product.get('product_title', 'N/A')}\n"
        f"Category: {product.get('product_category', 'N/A')}\n"
        f"Rating: {product.get('product_star_rating', 'N/A')} stars "
        f"({product.get('product_num_ratings', 'N/A')} ratings)\n"
        f"Price: {product.get('product_price', 'N/A')}\n"
        f"URL: {product.get('product_url', 'N/A')}\n"
    )

@mcp.tool()
async def getdata(
    prod: str,
    specific_features: str = "",
    minp: float = 1,
    maxp: float = 9999999.0
) -> Dict[str, Any]:
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": "520f2cc60amsh459728447612d24p1621fcjsn62b667fa8c78",
	    "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"

    }
    params = {
        "query": prod,
        "page": "1",
        "country": "IN",
        "sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE",
        "min_price":str(minp),
        "max_price":str(maxp)

    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        products = data.get("data", {}).get("products", [])
    summary=[]
    for i in products[:10]:
        summary.append(summarize_product(i))

    llmresponse= await decision_agent("\n".join(summary),prod,specific_features)    
    return llmresponse  

