import datetime
import math
import tweepy
import os

# === 設定 ===
START_DATETIME = datetime.datetime(2025, 9, 18, 9, 0)
END_DATETIME = datetime.datetime(2025, 12, 11, 9, 0)
TOTAL_SECONDS = (END_DATETIME - START_DATETIME).total_seconds()
TARGET_TIER = 999

# === 現在時刻 ===
now = datetime.datetime.now()

# === 経過・残り時間 ===
elapsed_seconds = (now - START_DATETIME).total_seconds()
progress_rate = min(elapsed_seconds / TOTAL_SECONDS * 100, 100)

remaining_seconds = TOTAL_SECONDS - elapsed_seconds
remaining_days = int(remaining_seconds // 86400)
remaining_hours = int((remaining_seconds % 86400) // 3600)
remaining_time_str = f"{remaining_days}日と約{remaining_hours}時間"

# === ティア計算 ===
current_tier = math.ceil(TARGET_TIER * elapsed_seconds / TOTAL_SECONDS)

tomorrow_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
if now.hour >= 9:
    tomorrow_9am += datetime.timedelta(days=1)
tomorrow_seconds = (tomorrow_9am - START_DATETIME).total_seconds()
tomorrow_tier = math.ceil(TARGET_TIER * tomorrow_seconds / TOTAL_SECONDS)

# === 投稿文（???回表示 削除済み）===
display_date = now.strftime('%Y/%m/%d')
post = f"""【シーズン7 集い築け！空飛ぶ探索拠点！】

ティア999進捗目安 9:00更新
《期間9/18～12/11 9時（確定）》

進捗率　{progress_rate:.1f}%
残り:{remaining_time_str}

本日9時時点目安ティア：{current_tier}
明日9時時点目標ティア：{tomorrow_tier}

#モンスターハンターnow
#モンハンNOW
#ティア進捗

9:00・{display_date}"""
