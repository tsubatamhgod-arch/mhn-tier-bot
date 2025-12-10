import datetime
import math
import tweepy
import os
import pytz

print("=== スクリプト開始 ===")

# === タイムゾーン設定 ===
JST = pytz.timezone("Asia/Tokyo")

# === シーズン8 日付設定（90日間） ===
START_DATETIME = JST.localize(datetime.datetime(2025, 12, 11, 9, 0))   # シーズン開始
END_DATETIME   = JST.localize(datetime.datetime(2026, 3, 11, 9, 0))    # 90日後終了
TOTAL_SECONDS = (END_DATETIME - START_DATETIME).total_seconds()
TARGET_TIER = 999

# === 現在時刻（毎朝9:00固定） ===
now = datetime.datetime.now(JST).replace(hour=9, minute=0, second=0, microsecond=0)
print(f"現在JST: {now}")

# === 経過・残り時間 ===
elapsed_seconds = (now - START_DATETIME).total_seconds()
progress_rate = min(max(elapsed_seconds / TOTAL_SECONDS * 100, 0), 100)

remaining_seconds = TOTAL_SECONDS - elapsed_seconds
remaining_days = max(int(remaining_seconds // 86400), 0)

# === ティア計算 ===
current_tier = max(min(math.ceil((TARGET_TIER * elapsed_seconds) / TOTAL_SECONDS), TARGET_TIER), 0)

tomorrow_9am = now + datetime.timedelta(days=1)
tomorrow_seconds = (tomorrow_9am - START_DATETIME).total_seconds()
tomorrow_tier = max(min(math.ceil((TARGET_TIER * tomorrow_seconds) / TOTAL_SECONDS), TARGET_TIER), 0)

# === 投稿文 ===
post = f"""【シーズン8 要撃用意！次元臨海の咆哮】

ティア999進捗目安（9:00更新）
《期間 12/11 9:00 ～ 3/11 9:00（90日間）》

進捗率　{progress_rate:.1f}%
残り: {remaining_days}日

本日9時時点目安ティア：{current_tier}
明日9時時点目標ティア：{tomorrow_tier}

#モンスターハンターNow
#モンハンNOW
#ティア進捗
#シーズン8"""

print("投稿文生成完了")

# === Tweepy認証 ===
print("APIキー確認:")
for key in ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]:
    print(f"  {key}: {'OK' if os.getenv(key) else 'NG'}")

client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY").strip(),
    consumer_secret=os.getenv("TWITTER_API_SECRET").strip(),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN").strip(),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET").strip()
)

# === 投稿実行 ===
try:
    print("投稿実行中...")
    response = client.create_tweet(text=post)
    tweet_id = response.data['id']
    print(f"投稿成功！ ID: {tweet_id}")
except Exception as e:
    print(f"投稿失敗: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
