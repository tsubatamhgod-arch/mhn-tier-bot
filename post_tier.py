import datetime
import math
import tweepy
import os

print("=== スクリプト開始 ===")

# === 設定 ===
START_DATETIME = datetime.datetime(2025, 9, 18, 9, 0)
END_DATETIME = datetime.datetime(2025, 12, 11, 9, 0)
TOTAL_SECONDS = (END_DATETIME - START_DATETIME).total_seconds()
TARGET_TIER = 999

# === 現在時刻 ===
now = datetime.datetime.now()
print(f"現在時刻: {now}")

# === 経過・残り時間 ===
elapsed_seconds = (now - START_DATETIME).total_seconds()
progress_rate = min(elapsed_seconds / TOTAL_SECONDS * 100, 100)

remaining_seconds = TOTAL_SECONDS - elapsed_seconds
remaining_days = int(remaining_seconds // 86400)  # 整数日数のみ
remaining_time_str = f"{remaining_days}日"

# === ティア計算 ===
current_tier = math.ceil(TARGET_TIER * elapsed_seconds / TOTAL_SECONDS)

tomorrow_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
if now.hour >= 9:
    tomorrow_9am += datetime.timedelta(days=1)
tomorrow_seconds = (tomorrow_9am - START_DATETIME).total_seconds()
tomorrow_tier = math.ceil(TARGET_TIER * tomorrow_seconds / TOTAL_SECONDS)

# === 日割りティア計算 ===
remaining_days_full = remaining_seconds / 86400
daily_tier = (TARGET_TIER - current_tier) / remaining_days_full if remaining_days_full > 0 else 0
daily_tier_rounded = round(daily_tier, 2)

# === 投稿文（日付・時間削除済み）===
post = f"""【シーズン7 集い築け！空飛ぶ探索拠点！】

ティア999進捗目安 9:00更新
《期間9/18～12/11 9時（確定）》

進捗率　{progress_rate:.1f}%
残り:{remaining_time_str}

本日9時時点目安ティア：{current_tier}
明日9時時点目標ティア：{tomorrow_tier}
1日あたり必要ティア：{daily_tier_rounded}

#モンスターハンターnow
#モンハンNOW
#ティア進捗"""
print("投稿文生成完了")

# === 環境変数チェック ===
print("APIキー確認:")
print(f"  TWITTER_API_KEY: {'OK' if os.getenv('TWITTER_API_KEY') else 'NG'}")
print(f"  TWITTER_API_SECRET: {'OK' if os.getenv('TWITTER_API_SECRET') else 'NG'}")
print(f"  TWITTER_ACCESS_TOKEN: {'OK' if os.getenv('TWITTER_ACCESS_TOKEN') else 'NG'}")
print(f"  TWITTER_ACCESS_TOKEN_SECRET: {'OK' if os.getenv('TWITTER_ACCESS_TOKEN_SECRET') else 'NG'}")

# === X API投稿 ===
print("Tweepyクライアント作成中...")
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

try:
    print("投稿実行中...")
    response = client.create_tweet(text=post)
    tweet_id = response.data['id']
    print(f"投稿成功！ ID: {tweet_id}")
    print(f"リンク: https://x.com/Shoyan_MonsterS/status/{tweet_id}")
except Exception as e:
    print(f"投稿失敗: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
