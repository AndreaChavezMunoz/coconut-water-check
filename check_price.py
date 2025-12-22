import os
import requests


# ---------- CONFIG ----------
PRODUCT_ID = "573570"
SALES_CHANNEL = 70
PRODUCT_URL = "https://www.wong.pe/agua-de-coco-natifrut-300ml-701143-2/p?srsltid=AfmBOopHG5FLpp9qAWhE-CVbkNimhrIlwSc_Ymqiz0QwMBOu41vDnPMW"
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN")



# ---------- PRICE FETCH ----------
def fetch_price_from_vtex_api(product_id: str, sales_channel: int) -> float:
    url = (
        "https://www.wong.pe/api/catalog_system/pub/products/search"
        f"?sc={sales_channel}&fq=productId:{product_id}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    offer = data[0]["items"][0]["sellers"][0]["commertialOffer"]
    return offer["Price"]


# ---------- PUSH NOTIFICATION ----------
def send_push_notification(price: float) -> None:
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_APP_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": "🥥 Precio cambió",
            "message": f"Nuevo precio: S/ {price}",
            "url": "https://www.wong.pe/coconut-water",
            "url_title": "Ver producto en Wong",
        },
        timeout=10
    )

    print("Pushover status:", response.status_code)
    print("Pushover response:", response.text)


# ---------- MAIN ----------
def main():
    price = fetch_price_from_vtex_api(PRODUCT_ID, SALES_CHANNEL)
    print(f"Current price: S/ {price:.2f}")

    send_push_notification(price)


if __name__ == "__main__":
    main()
