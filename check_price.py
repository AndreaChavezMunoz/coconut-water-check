import os
import requests


# ---------- CONFIG ----------
PRODUCT_ID = "573570"
SALES_CHANNEL = 70
PRODUCT_URL = "https://www.wong.pe/agua-de-coco-natifrut-300ml-701143-2/p?srsltid=AfmBOopHG5FLpp9qAWhE-CVbkNimhrIlwSc_Ymqiz0QwMBOu41vDnPMW"
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN")
PRICE_THRESHOLD = 7.00  # Only send notification if price < S/ 7


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
def send_push_notification(price):
    token = PUSHOVER_APP_TOKEN
    user = PUSHOVER_USER_KEY

    if not token or not user:
        raise RuntimeError("Missing Pushover credentials")

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": token,
            "user": user,
            "title": "🥥 PRECIO BAJO!",
            "message": f"¡Oferta! Agua de coco a S/ {price:.2f}",
            "url": PRODUCT_URL,
            "url_title": "Ver producto en Wong",
            "priority": 1,  # Optional: makes the notification stand out more
        },
        timeout=10
    )

    print("Pushover status:", response.status_code)
    print("Pushover response:", response.text)


# ---------- MAIN ----------
def main():
    price = fetch_price_from_vtex_api(PRODUCT_ID, SALES_CHANNEL)
    print(f"Current price: S/ {price:.2f}")
    
    # Check if price is below threshold
    if price < PRICE_THRESHOLD:
        print(f"✅ Price is below S/ {PRICE_THRESHOLD:.2f}! Sending notification...")
        send_push_notification(price)
    else:
        print(f"❌ Price is S/ {price:.2f} (not below S/ {PRICE_THRESHOLD:.2f}). No notification sent.")


if __name__ == "__main__":
    # Quick check for debugging
    if not PUSHOVER_USER_KEY or not PUSHOVER_APP_TOKEN:
        print("⚠️  Warning: Pushover credentials not set")
        print(f"   PUSHOVER_USER_KEY: {'Set' if PUSHOVER_USER_KEY else 'Not set'}")
        print(f"   PUSHOVER_APP_TOKEN: {'Set' if PUSHOVER_APP_TOKEN else 'Not set'}")
    else:
        print("✅ Pushover credentials are set")
    
    main()