import requests


def fetch_price_from_vtex_api(product_id: str, sales_channel: int = 70) -> float:
    """Fetch product price from VTEX catalog API."""
    url = (
        "https://www.wong.pe/api/catalog_system/pub/products/search"
        f"?sc={sales_channel}&fq=productId:{product_id}"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return data[0]["items"][0]["sellers"][0]["commertialOffer"]["Price"]


def main():
    product_id = "573570"  # Coconut water product ID
    price = fetch_price_from_vtex_api(product_id)

    print(f"Current price: S/ {price:.2f}")


if __name__ == "__main__":
    main()
