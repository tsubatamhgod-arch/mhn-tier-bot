import datetime
import math
import tweepy
import os
import pytz

print("=== スクリプト開始 ===")

# === タイムゾーン設定 ===
JST = pytz.timezone("Asia/Tokyo")
now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
now_jst = now_utc.astimezone(JST)

# === 今日の9:00（JST）を明確に算出 ===
today_9am = now_jst.replace(hour=9, minute=0, second=0, microsecond=0)

# 実行が9時以降でも未満でも「毎朝9:00基準」で固定
now = today_9am

print(f"現在UTC: {now_utc}")
print(f"現在JST: {now_jst}")
print(f"使用する基準時刻（JST 毎朝 9:00 固定）: {now}")

# === 期間設定 ===
START_DATETIME = JST.localize(datetime.datetime(2025, 9, 18, 9, 0))
END_DATETIME   = JST.localize(datetime.datetime(2025, 12, 11, 9, 0))
TOTAL_SECONDS = (END_DATETIME - START_DATETIME).total_seconds()
TARGET_TIER = 999

# === 経過時間・残り時間計算 ===
elapsed_seconds = (now - START_DATETIME).total_seconds()
progress_rate = min(elapsed_seconds / TOTAL_SECONDS * 100, 100)

remaining_seconds = TOTAL_SECONDS - elapsed_seconds
remaining_days = max(int(remaining_seconds // 86400), 0)

# === ティア計算 ===
current_tier = max(math.ceil((TARGET_TIER * elapsed_seconds) / TOTAL_SECONDS), 0)

# 明日9:00（毎朝基準なので now +1日）
tomorrow_9am = now + datetime.timedelta(days=1)
tomorrow_seconds = (tomorrow_9am - START_DATETIME).total_seconds()
tomorrow_tier = max(math.ceil((TARGET_TIER * tomorrow_seconds) / TOTAL_SECONDS), 0)

# 1日の必要ティア
if remaining_seconds > 0:
    daily_tier = (TARGET_TIER - current_tier) / (remaining_seconds / 86400)
    daily_tier_rounded = round(daily_tier, 2)
else:
    daily_tier_rounded = 0

# === 投稿文（「毎朝9:00更新」を明示） ===
post = f"""【シーズン7 集い築け！空飛ぶ探索拠点！】

ティア999進捗目安（毎朝9:00更新 / JST）
《期間 9/18 ～ 12/11 9時（確定）》

進捗率　{progress_rate:.1f}%
残り: {remaining_days}日

本日（毎朝）9時時点目安ティア：{current_tier}
明日9時時点目標ティア：{tomorrow_tier}
1日あたり必要ティア：{daily_tier_rounded}

#モンスターハンターnow
#モンハンNOW
#ティア進捗"""

print("投稿文生成完了")

# === APIキー確認 ===
print("APIキー確認:")
print(f"  TWITTER_API_KEY: {'OK' if os.getenv('TWITTER_API_KEY') else 'NG'}")
print(f"  TWITTER_API_SECRET: {'OK' if os.getenv('TWITTER_API_SECRET') else 'NG'}")
print(f"  TWITTER_ACCESS_TOKEN: {'OK' if os.getenv('TWITTER_ACCESS_TOKEN') else 'NG'}")
print(f"  TWITTER_ACCESS_TOKEN_SECRET: {'OK' if os.getenv('TWITTER_ACCESS_TOKEN_SECRET') else 'NG'}")

# === Xへ投稿 ===
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
