import requests
import hashlib

# ====== КОНФИГУРАЦИЯ ======
BOT_TOKEN = "ВАШ_ТОКЕН_ТЕЛЕГРАМ"

# Бесплатные API ключи (зарегистрируйтесь сами)
NUMVERIFY_API_KEY = "ваш_ключ_numverify"   # https://numverify.com (бесплатно 100 запросов/мес)
HIBP_API_KEY = "ваш_ключ_hibp"             # https://haveibeenpwned.com (не обязателен)

# ====== 1. ОПРЕДЕЛЕНИЕ ОПЕРАТОРА И РЕГИОНА ======
def get_operator(phone):
    # numverify (бесплатный, но требует ключ)
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone}&format=1"
    try:
        resp = requests.get(url, timeout=5).json()
        if resp.get("valid"):
            return f"Оператор: {resp.get('carrier', 'неизвестно')}, Страна: {resp.get('country_name', '')}, Регион: {resp.get('location', '')}"
        else:
            return "Номер не валиден или информация недоступна."
    except:
        return "Не удалось определить оператора (проверьте ключ)."

# ====== 2. ПРОВЕРКА УТЕЧЕК ======
def check_breaches(phone):
    # Переводим номер в хеш для HIBP (только если номер участвовал в утечках)
    # Просто пример – реально HIBP работает по email, но можно расширить
    # Для демонстрации используем заглушку
    return "Утечек в открытых базах не найдено (эмуляция)."

# ====== 3. ПОИСК В СОЦСЕТЯХ (VK, Telegram) ======
def search_social(phone):
    result = []
    # VK API (открытый поиск по номеру, требует токен)
    # https://vk.com/dev/users.search?params=phone
    vk_token = "ваш_токен_vk"  # получить в VK API
    if vk_token != "ваш_токен_vk":
        try:
            url = f"https://api.vk.com/method/users.search?q={phone}&access_token={vk_token}&v=5.131"
            resp = requests.get(url, timeout=5).json()
            if resp.get("response"):
                items = resp["response"].get("items", [])
                for user in items[:3]:
                    result.append(f"VK: {user.get('first_name', '')} {user.get('last_name', '')} (id: {user.get('id')})")
            else:
                result.append("VK: не найдено")
        except:
            result.append("VK: ошибка запроса")
    else:
        result.append("VK: не настроен (нужен токен)")

    # Telegram – через бота @userinfobot или поиск по номеру (неофициально)
    # Используем публичный сервис (например, tgscan) – эмуляция
    result.append("Telegram: привязка не проверена (API нет)")

    return "\n".join(result) if result else "Соцсети: не найдено."

# ====== 4. ОБЩАЯ СВОДКА ======
def get_full_info(phone):
    lines = []
    lines.append(f"📱 Номер: {phone}")
    lines.append("")
    lines.append("【Оператор】")
    lines.append(get_operator(phone))
    lines.append("")
    lines.append("【Утечки】")
    lines.append(check_breaches(phone))
    lines.append("")
    lines.append("【Соцсети】")
    lines.append(search_social(phone))
    lines.append("")
    lines.append("⚠️ Данные собраны из открытых источников.\nПолнота зависит от наличия API-ключей.")
    return "\n".join(lines)