import requests

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    try:
        # Test categorías
        response = requests.get(f"{BASE_URL}/api/categorias")
        print(f"✅ Categorías - Status: {response.status_code}")
        print(f"📊 Response: {response.json()}")
        
        # Test raíz
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Raíz - Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()