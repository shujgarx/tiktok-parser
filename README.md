# 🎯 TikTok Video Info (Async) — `tiktok_pars.py`

Небольшой асинхронный скрипт на Python для получения полной информации о ролике TikTok через библиотеку **[`TikTokApi`](https://pypi.org/project/TikTokApi/)** и сохранения результата в `JSON`.

> Скрипт вытягивает `video_id` из URL, запрашивает подробные метаданные и сохраняет их в файл `video_<ID>.json`.

---

## ⚡ Возможности

* Извлекает `video_id` из любого URL TikTok (`/video/<id>`).
* Получает полную «сыровую» структуру данных (`.info()`).
* Печатает результат в консоль **и** сохраняет в файл.
* Работает стабильнее при передаче cookie `ms_token`.

---

## 🧩 Что внутри

Файл: **`tiktok_pars.py`**

Ключевые части:

* `extract_video_id(url)` — достаёт числовой ID ролика из пути `/video/<id>`.
* `main()` — создаёт Playwright-сессию через `TikTokApi`, запрашивает `video.info()`, печатает и сохраняет результат.
* Переменная окружения **`ms_token`** (необязательно, но сильно повышает стабильность).

---

## 📦 Установка

Требования: **Python 3.9+** (рекомендуется 3.10/3.11)

```bash
# Установите зависимости
pip install --upgrade pip
pip install TikTokApi playwright

# Установите браузер для Playwright
python -m playwright install chromium
```

> Если используете **poetry/requirements.txt**, просто добавьте пакеты `TikTokApi` и `playwright`, а затем выполните `playwright install chromium`.

---

## 🔐 `ms_token`: что это и где взять

`ms_token` — это cookie из браузера, которая помогает эмулировать реальную сессию и повысить вероятность успешного ответа без CAPTCHA/403.

1. Зайдите на `tiktok.com` в обычном браузере.
2. Откройте Инструменты разработчика → Application/Storage → Cookies → `https://www.tiktok.com`.
3. Найдите cookie **`msToken`**, скопируйте значение.
4. Экспортируйте в окружение перед запуском скрипта:

**macOS / Linux (bash/zsh):**

```bash
export ms_token="ВАШ_MS_TOKEN"
```

**Windows (PowerShell):**

```powershell
$env:ms_token="ВАШ_MS_TOKEN"
```

> Можно запускать и без токена (в коде допускается `None`), но с токеном стабильнее.

---

## 🚀 Запуск

В коде уже задан пример URL:

```python
VIDEO_URL = "https://www.tiktok.com/@ssshiabrb8999/video/7534792128535284997?is_from_webapp=1&sender_device=pc"
```

При необходимости просто замените `VIDEO_URL` на нужный.

Далее запустите:

```bash
python tiktok_pars.py
```

**Что произойдёт:**

* В консоли увидите ID ролика и JSON с данными.
* В текущей папке появится файл `video_<ID>.json`.

Пример вывода (усечён):

```text
[i] video_id: 7534792128535284997
{
  "id": "7534792128535284997",
  "desc": "...",
  "createTime": "172... ",
  "author": { "...": "..." },
  "music": { "...": "..." },
  "stats": {
    "playCount": 12345,
    "diggCount": 678,
    "commentCount": 90,
    "shareCount": 12
  },
  ...
}
[✓] Данные сохранены в video_7534792128535284997.json
```

---

## ⚙️ Как это работает

* `async with TikTokApi() as api:` — инициализация клиента.
* `api.create_sessions(...)` — создаёт сессию Playwright (браузер: `chromium`).
* `await api.video(id=..., url=...).info()` — получает полную структуру данных ролика.
* Унификация ответа: библиотека может вернуть объект с `.as_dict`; код приводит к `dict`.

---

## 🌐 Прокси (опционально)

Если сталкиваетесь с частыми 403/CAPTCHA или региональными блокировками, используйте прокси:

```python
await api.create_sessions(
    ms_tokens=[MS_TOKEN],
    num_sessions=1,
    sleep_after=3,
    browser="chromium",
    # proxy="http://user:pass@host:port"  # пример
)
```

Также можно задавать прокси через переменные окружения (`HTTP_PROXY`, `HTTPS_PROXY`).

---

## 🧪 Советы по стабильности

* Актуализируйте пакеты: `pip install -U TikTokApi playwright`.
* Убедитесь, что установлен браузер: `python -m playwright install chromium`.
* Меняйте/обновляйте `ms_token`, если начались ошибки 403/вызовы CAPTCHA.
* Избегайте слишком частых запросов подряд — соблюдайте паузы.

---



> Замените `\<Ваше имя\>` на ваше имя/название компании. Рекомендуется также положить текст лицензии отдельным файлом **`LICENSE`** в корень репозитория.
