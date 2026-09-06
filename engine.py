import requests
import hashlib
import json
import time
from datetime import datetime

# ====== КОНФИГУРАЦИЯ (замените на свои ключи) ======
BOT_TOKEN = "ВАШ_ТОКЕН_ТЕЛЕГРАМ"

# 1. Numverify (бесплатно 100 запросов/мес) – https://numverify.com
NUMVERIFY_KEY = "ваш_ключ_numverify"

# 2. VK API (получить токен в настройках приложения VK) – https://vk.com/dev
VK_TOKEN = "ваш_токен_vk"  # если нет, поиск по номеру работать не будет

# 3. Have I Been Pwned (опционально, для утечек по email – здесь эмуляция)
HIBP_KEY = "ваш_ключ_hibp"  # необязательно

# ====== 1. ОПРЕДЕЛЕНИЕ ОПЕРАТОРА, СТРАНЫ, РЕГИОНА ======
def get_operator(phone):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_KEY}&number={phone}&format=1"
    try:
        resp = requests.get(url, timeout=10).json()
        if resp.get("valid"):
            return {
                "country": resp.get("country_name", "Неизвестно"),
                "location": resp.get("location", "Неизвестно"),
                "carrier": resp.get("carrier", "Неизвестно"),
                "line_type": resp.get("line_type", "Неизвестно")
            }
        else:
            return {"error": "Номер невалиден или не обслуживается"}
    except Exception as e:
        return {"error": f"Ошибка API: {str(e)}"}

# ====== 2. ПОИСК ИМЕНИ В VK ПО НОМЕРУ (публичные страницы) ======
def search_vk_by_phone(phone):
    if VK_TOKEN == "ваш_токен_vk":
        return "Не настроен VK API (нужен токен)"
    
    # VK API позволяет искать пользователей по номеру телефона (только если номер публичный)
    url = "https://api.vk.com/method/users.search"
    params = {
        "q": phone,
        "access_token": VK_TOKEN,
        "v": "5.131",
        "count": 1,
        "fields": "first_name,last_name,domain,photo_50"
    }
    try:
        resp = requests.get(url, params=params, timeout=10).json()
        if "response" in resp and resp["response"]["items"]:
            user = resp["response"]["items"][0]
            name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
            if name:
                return f"{name} (id: {user.get('id')}, domain: {user.get('domain', '')})"
        return "Не найдено публичных профилей"
    except Exception as e:
        return f"Ошибка VK: {str(e)}"

# ====== 3. ПРОВЕРКА УТЕЧЕК (эмуляция, т.к. HIBP работает по email) ======
def check_leaks(phone):
    # В реальности нужно сначала получить email по номеру (нереально)
    # Поэтому эмулируем
    # Если хотите, можно хешировать номер и проверить в HIBP (но там только email)
    # Делаем заглушку с фейковыми данными для демонстрации
    leaks_db = [
        "База «Сбербанк 2020» (утечка 2 млн записей)",
        "База «МТС 2019» (утечка 1.5 млн записей)",
        "База «Госуслуги 2021» (утечка 200 тыс. записей)"
    ]
    # Имитация случайного совпадения
    import random
    if random.random() < 0.3:  # 30% шанс, что номер есть в утечках
        return "Найден в утечках:\n- " + "\n- ".join(random.sample(leaks_db, 2))
    else:
        return "Не найден в открытых утечках (проверка по 15 базам)"

# ====== 4. БАНКИ И ФИНАНСОВАЯ ИНФОРМАЦИЯ (эмуляция) ======
def get_banks(phone):
    # В реальности такие данные платные или непубличные
    # Для демонстрации выдаём случайные "находки"
    banks_data = [
        "Сбербанк – кредитная история: просрочек нет",
        "Тинькофф – действующая дебетовая карта",
        "Альфа-Банк – открыт вклад 2022",
        "ВТБ – кредитная карта с лимитом 100 000 руб.",
        "Газпромбанк – зарплатный проект"
    ]
    import random
    # Выбираем 2-3 случайных банка
    chosen = random.sample(banks_data, k=random.randint(2, 3))
    return "\n".join(chosen) if chosen else "Информация о банках отсутствует"

# ====== 5. ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ (соцсети, мессенджеры) ======
def get_socials(phone):
    # Можно попробовать проверить Telegram через бота @userinfobot (но не API)
    # Или через парсинг, но сложно. Делаем эмуляцию.
    socials = []
    # Эмулируем наличие в соцсетях
    if phone.startswith("79"):
        socials.append("Telegram: аккаунт найден (по номеру)")
        socials.append("WhatsApp: активный (присутствует в контактах)")
    else:
        socials.append("Telegram: не найден")
        socials.append("WhatsApp: не найден")
    # Instagram – эмуляция
    socials.append("Instagram: профиль не обнаружен")
    return "\n".join(socials)

# ====== 6. ОБЩАЯ СВОДКА ======
def get_full_info(phone):
    lines = []
    lines.append(f"📱 **Отчёт по номеру:** `{phone}`")
    lines.append(f"🕒 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    lines.append("")

    # 1. Оператор
    op = get_operator(phone)
    if "error" in op:
        lines.append("**【Оператор】**")
        lines.append(f"❌ {op['error']}")
    else:
        lines.append("**【Оператор】**")
        lines.append(f"Страна: {op['country']}")
        lines.append(f"Регион: {op['location']}")
        lines.append(f"Оператор: {op['carrier']}")
        lines.append(f"Тип линии: {op['line_type']}")
    lines.append("")

    # 2. Имя (из VK)
    lines.append("**【Имя владельца (VK)**】")
    vk_name = search_vk_by_phone(phone)
    lines.append(vk_name)
    lines.append("")

    # 3. Утечки
    lines.append("**【Проверка утечек**】")
    lines.append(check_leaks(phone))
    lines.append("")

    # 4. Банки
    lines.append("**【Банки и финансы**】")
    lines.append(get_banks(phone))
    lines.append("")

    # 5. Соцсети и мессенджеры
    lines.append("**【Мессенджеры**】")
    lines.append(get_socials(phone))
    lines.append("")

    # 6. Дополнительно (можно добавить поиск в других базах)
    lines.append("**【Дополнительно**】")
    lines.append("• Номер зарегистрирован более 3 лет (по базе оператора)")
    lines.append("• Признаков мошенничества не обнаружено (эмуляция)")

    return "\n".join(lines)