import requests
import yaml

# 🔹 Ссылка на YAML-файл на GitHub
GITHUB_YAML_URL = "https://raw.githubusercontent.com/wedlex/trading_config/main/active_pairs.yaml"

# 🔹 Ссылка на Bybit API (получение списка всех пар)
BYBIT_API_URL = "https://api.bybit.com/v5/market/tickers?category=linear"

def load_yaml():
    """Загружаем active_pairs.yaml из GitHub"""
    response = requests.get(GITHUB_YAML_URL, timeout=10)
    response.raise_for_status()
    return yaml.safe_load(response.text)

def get_bybit_pairs():
    """Получаем список всех доступных пар на Bybit"""
    response = requests.get(BYBIT_API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "result" in data and "list" in data["result"]:
        return {item["symbol"] for item in data["result"]["list"]}

    return set()

def validate_pairs():
    """Проверяем, что все пары из active_pairs.yaml есть на Bybit"""
    yaml_data = load_yaml()
    bybit_pairs = get_bybit_pairs()

    active_pairs = set(yaml_data.get("pairs", {}).get("bybit", []))  # Берем только пары Bybit
    invalid_pairs = active_pairs - bybit_pairs  # Какие пары указаны, но их нет на бирже

    if invalid_pairs:
        print(f"❌ Ошибка! Эти пары отсутствуют на Bybit: {invalid_pairs}")
    else:
        print("✅ Все пары в active_pairs.yaml существуют на Bybit!")

# 🔹 Запускаем проверку
validate_pairs()
