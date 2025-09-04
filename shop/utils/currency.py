import requests
import logging 

# Создаем логгер специально для этого модуля.
# Это хорошая практика, чтобы в логах было видно, откуда пришло сообщение.
log = logging.getLogger(__name__)

# Используем бесплатный API, который не требует ключей
API_URL = "https://open.er-api.com/v6/latest/RUB"

def convert_rub_to(currency: str, amount: float) -> float | None:
    """Конвертирует сумму в рублях в другую валюту."""
    currency = currency.upper()
    log.info(f"Запрос на конвертацию {amount} RUB в {currency}")
     
    try:
        response = requests.get(API_URL)
        # Проверяем, что запрос успешен (код 200)
        response.raise_for_status() 
        
        data = response.json()
        rates = data.get("rates")
        
        if not rates or currency not in rates:
            log.error(f"Валюта '{currency}' не найдена в курсах API.")
            return None
            
        rate = rates[currency]
        result = round(amount * rate, 2)
        log.info(f"Конвертация успешна: {amount} RUB = {result} {currency}")
        return result

    except requests.RequestException as e:
        log.error(f"Ошибка сети при получении курсов валют: {e}", exc_info=True)
        return None
