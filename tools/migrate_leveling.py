import sqlite3
import json
import os

OLD_DIR = "Old_DB"
NEW_DB = "databases/leveling.db"

LEVELS_AND_XP = {
    "0": 0, "1": 100, "2": 255, "3": 475, "4": 770, "5": 1150, "6": 1625, "7": 2205, "8": 2900, "9": 3720,
    "10": 4675, "11": 5775, "12": 7030, "13": 8450, "14": 10045, "15": 11825, "16": 13800, "17": 15980, "18": 18375, "19": 20995,
    "20": 23850, "21": 26950, "22": 30305, "23": 33925, "24": 37820, "25": 42000, "26": 46475, "27": 51255, "28": 56350, "29": 61770,
    "30": 67525, "31": 73625, "32": 80080, "33": 86900, "34": 94095, "35": 101675, "36": 109650, "37": 118030, "38": 126825, "39": 136045,
    "40": 145700, "41": 155800, "42": 166355, "43": 177375, "44": 188870, "45": 200850, "46": 213325, "47": 226305, "48": 239800, "49": 253820,
    "50": 268375, "51": 283475, "52": 299130, "53": 315350, "54": 332145, "55": 349525, "56": 367500, "57": 386080, "58": 405275, "59": 425095,
    "60": 445550, "61": 466650, "62": 488405, "63": 510825, "64": 533920, "65": 557700, "66": 582175, "67": 607355, "68": 633250, "69": 659870,
    "70": 687225, "71": 715325, "72": 744180, "73": 773800, "74": 804195, "75": 835375, "76": 867350, "77": 900130, "78": 933725, "79": 968145,
    "80": 1003400, "81": 1039500, "82": 1076455, "83": 1114275, "84": 1152970, "85": 1192550, "86": 1233025, "87": 1274405, "88": 1316700, "89": 1359920,
    "90": 1404075, "91": 1449175, "92": 1495230, "93": 1542250, "94": 1590245, "95": 1639225, "96": 1689200, "97": 1740180, "98": 1792175, "99": 1845195,
    "100": 1899250,
}

def migrate():
    if not os.path.exists(NEW_DB):
        print(f"Error: New database {NEW_DB} does not exist. Run setup.py first.")
        return

    new_conn = sqlite3.connect(NEW_DB)
    new_cur = new_conn.cursor()

    # 1. Migrate ignored channels
    old_ignore_path = os.path.join(OLD_DIR, "xp_ignore.db")
    if os.path.exists(old_ignore_path):
        try:
            ignore_conn = sqlite3.connect(old_ignore_path)
            ignore_cur = ignore_conn.cursor()
            ignore_cur.execute("SELECT guild_id, channel_id FROM xp_ignore")
            rows = ignore_cur.fetchall()
            
            for guild_id, channel_id in rows:
                new_cur.execute("INSERT OR IGNORE INTO ignored_channels (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
            print(f"✅ Migrated {len(rows)} ignored channels from {old_ignore_path}")
        except Exception as e:
            print(f"❌ Error migrating {old_ignore_path}: {e}")
    else:
        print(f"ℹ️ {old_ignore_path} not found. Skipping ignored channels migration.")

    # 2. Migrate guild toggle settings
    old_json_path = os.path.join(OLD_DIR, "leveling.json")
    if os.path.exists(old_json_path):
        try:
            with open(old_json_path, "r") as f:
                data = json.load(f)
            
            for guild_id, enabled in data.items():
                new_cur.execute(
                    "INSERT INTO guild_config (guild_id, enabled) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET enabled = excluded.enabled",
                    (int(guild_id), 1 if enabled else 0)
                )
            print(f"✅ Migrated {len(data)} guild toggles from {old_json_path}")
        except Exception as e:
            print(f"❌ Error migrating {old_json_path}: {e}")
    else:
        print(f"ℹ️ {old_json_path} not found. Skipping guild toggles migration.")

    # 3. Migrate wipe toggle settings
    old_wipe_path = os.path.join(OLD_DIR, "leveling_wipe_toggle.db")
    if os.path.exists(old_wipe_path):
        try:
            wipe_conn = sqlite3.connect(old_wipe_path)
            wipe_cur = wipe_conn.cursor()
            wipe_cur.execute("SELECT guild_id, status FROM xp_wipe_onleave")
            rows = wipe_cur.fetchall()
            
            for guild_id, status in rows:
                # Old code: status 0 = wipe enabled. New code: wipe_on_leave 1 = enabled
                wipe_val = 1 if status == 0 else 0
                new_cur.execute(
                    "INSERT INTO guild_config (guild_id, wipe_on_leave) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET wipe_on_leave = excluded.wipe_on_leave",
                    (int(guild_id), wipe_val)
                )
            print(f"✅ Migrated {len(rows)} wipe toggles from {old_wipe_path}")
        except Exception as e:
            print(f"❌ Error migrating {old_wipe_path}: {e}")
    else:
        print(f"ℹ️ {old_wipe_path} not found. Skipping wipe toggles migration.")

    # 4. Migrate user XP
    old_lvl_path = os.path.join(OLD_DIR, "DiscordLevelingSystem.db")
    if os.path.exists(old_lvl_path):
        try:
            lvl_conn = sqlite3.connect(old_lvl_path)
            lvl_cur = lvl_conn.cursor()
            
            lvl_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in lvl_cur.fetchall()]
            
            target_table = None
            for t in tables:
                if t.lower() in ('discordlevelingsystem', 'leveling', 'users'):
                    target_table = t
                    break
                    
            if target_table:
                lvl_cur.execute(f"PRAGMA table_info({target_table})")
                columns = [row[1] for row in lvl_cur.fetchall()]
                
                guild_col = next((c for c in columns if 'guild' in c.lower()), 'guild_id')
                user_col = next((c for c in columns if 'user' in c.lower() or 'member' in c.lower()), 'user_id')
                xp_col = next((c for c in columns if 'total' in c.lower() or 'xp' in c.lower()), 'xp')
                lvl_col = next((c for c in columns if 'level' in c.lower()), 'level')
                
                lvl_cur.execute(f"SELECT {guild_col}, {user_col}, {xp_col}, {lvl_col} FROM {target_table}")
                rows = lvl_cur.fetchall()
                
                migrated = 0
                for g_id, u_id, total_xp, level in rows:
                    if not g_id or not u_id: continue
                    
                    # Calculate progress xp using the old LEVELS_AND_XP dictionary
                    base_xp = LEVELS_AND_XP.get(str(level), 0)
                    progress_xp = max(0, int(total_xp) - base_xp)
                    
                    new_cur.execute(
                        "INSERT OR REPLACE INTO user_levels (guild_id, user_id, xp, level, total_xp) VALUES (?, ?, ?, ?, ?)",
                        (int(g_id), int(u_id), progress_xp, int(level), int(total_xp))
                    )
                    migrated += 1
                print(f"✅ Migrated {migrated} user levels from {old_lvl_path} (table {target_table})")
            else:
                print(f"❌ Could not determine table name in {old_lvl_path}")
        except Exception as e:
            print(f"❌ Error migrating {old_lvl_path}: {e}")
    else:
        print(f"ℹ️ {old_lvl_path} not found. Skipping user XP migration.")
            
    new_conn.commit()
    new_conn.close()
    print("🚀 Migration complete! The old leveling data is now successfully imported into databases/leveling.db")

if __name__ == "__main__":
    migrate()