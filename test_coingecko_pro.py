"""
Test CoinGecko Pro API Integration
===================================
Quick test to verify the API key is working correctly
"""

import os
import sys
import requests

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("[WARN] python-dotenv not installed. Using system environment variables.")

def test_api_connection():
    """Test CoinGecko Pro API connection"""

    api_key = os.getenv("COINGECKO_PRO_API_KEY")

    if not api_key:
        print("❌ COINGECKO_PRO_API_KEY not found in environment variables")
        print("   Make sure .env file exists with your API key")
        return False

    print(f"✅ Found API key: {api_key[:8]}...{api_key[-4:]}")

    # Test 1: Simple price query
    print("\n📊 Test 1: Fetching BTC and ETH prices...")
    try:
        url = "https://pro-api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum',
            'vs_currencies': 'usd',
            'x_cg_pro_api_key': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        print(f"   ✅ Bitcoin: ${data['bitcoin']['usd']:,.2f}")
        print(f"   ✅ Ethereum: ${data['ethereum']['usd']:,.2f}")

    except requests.exceptions.HTTPError as e:
        print(f"   ❌ HTTP Error: {e}")
        print(f"   Status Code: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    # Test 2: Market data query
    print("\n📈 Test 2: Fetching top 10 coins by market cap...")
    try:
        url = "https://pro-api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'x_cg_pro_api_key': api_key
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        coins = response.json()
        print(f"   ✅ Retrieved {len(coins)} coins:")
        for i, coin in enumerate(coins[:5], 1):
            print(f"      {i}. {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:,.2f}")

    except requests.exceptions.HTTPError as e:
        print(f"   ❌ HTTP Error: {e}")
        print(f"   Status Code: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED! CoinGecko Pro API is working correctly.")
    print("="*80)
    return True


if __name__ == "__main__":
    print("="*80)
    print("COINGECKO PRO API TEST")
    print("="*80)

    success = test_api_connection()

    if success:
        print("\n✅ Ready to use ai_competition_automation.py with Pro API!")
    else:
        print("\n❌ Please fix the issues above before using the automation script.")
