import requests

BASE_URL = "https://dummyjson.com/products"


def get_all_products():
    """
    Get ALL products (default = first 30)
    """
    response = requests.get(BASE_URL)
    response.raise_for_status()

    data = response.json()
    return data["products"], data["total"]


def get_single_product(product_id):
    """
    Get a SINGLE product by ID
    """
    response = requests.get(f"{BASE_URL}/{product_id}")
    response.raise_for_status()

    return response.json()


def get_products_with_limit(limit=100):
    """
    Get specific number of products
    """
    response = requests.get(f"{BASE_URL}?limit={limit}")
    response.raise_for_status()

    data = response.json()
    return data["products"], data["total"]


def search_products(query):
    """
    Search products by keyword
    """
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    response.raise_for_status()

    data = response.json()
    return data["products"], data["total"]

# Task 3.1:
# (a) Fetch_all_products:
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()  # raises error for 4xx/5xx

        data = response.json()
        products = data.get("products", [])

        cleaned_products = []

        for product in products:
            cleaned_products.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        print(f"✅ Successfully fetched {len(cleaned_products)} products")
        return cleaned_products

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch products from API")
        print("Error:", e)
        return []
    
# (b) Create_Product_Mapping:
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    print(f"✅ Product mapping created for {len(product_mapping)} products")
    return product_mapping


