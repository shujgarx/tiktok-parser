# testparcer.py
import asyncio, os, re, json
from TikTokApi import TikTokApi

VIDEO_URL = "https://www.tiktok.com/@ssshiabrb8999/video/7534792128535284997?is_from_webapp=1&sender_device=pc"
MS_TOKEN = os.environ.get("ms_token", None)

def extract_video_id(url: str) -> str:
    m = re.search(r"/video/(\d+)", url)
    if not m:
        raise ValueError("Не удалось вытащить video_id из URL")
    return m.group(1)

async def main():
    vid = extract_video_id(VIDEO_URL)
    print(f"[i] video_id: {vid}")

    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[MS_TOKEN],   # можно оставить [None], но с токеном стабильнее
            num_sessions=1,
            sleep_after=3,
            browser="chromium",     # у тебя Chrome — ок, chromium подойдёт
        )

        # Важно: передаём и id, и url
        resp = await api.video(id=vid, url=VIDEO_URL).info()

        # Унифицируем под разные версии библиотеки:
        data = getattr(resp, "as_dict", resp)

        print(json.dumps(data, ensure_ascii=False, indent=2))

        out_name = f"video_{vid}.json"
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[✓] Данные сохранены в {out_name}")

if __name__ == "__main__":
    asyncio.run(main())
