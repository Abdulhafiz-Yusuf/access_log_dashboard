# generate_access_logs.py
# ------------------------------------------------------------
# Hands-on: Create a realistic access_logs.csv (500-1000 rows)
# ------------------------------------------------------------
import os
import csv                     # write CSV files
import random                  # random choices & numbers
from datetime import datetime, timedelta
from faker import Faker        # realistic fake names, IPs, etc.

# ------------------------------------------------------------
# 1. SETTINGS – change only these if you want different data
# ------------------------------------------------------------
NUM_ROWS = 998                # <-- 500-1000 rows
SEED = 42                      # reproducible output
OUTPUT_FILE = "data/access_logs.csv"

# ------------------------------------------------------------
# 2. INITIALISE helpers
# ------------------------------------------------------------
random.seed(SEED)              # same data every run
fake = Faker()
Faker.seed(SEED)

# Lists of possible values (real-world variety)
USERNAMES = [fake.user_name() for _ in range(120)]   # ~120 unique users
BRANCHES  = ["Gusau", "Kano", "Lagos", "Abuja", "Port Harcourt", "Ibadan"]
ROLES     = ["Teller", "Ops", "IT", "Security"]
DEVICE_TYPES = ["Desktop", "Mobile"]
STATUSES  = ["SUCCESS", "FAILED"]

# ------------------------------------------------------------
# 3. Helper: random timestamp in a workday (08:00-18:00)
# ------------------------------------------------------------
def random_workday_timestamp(start_hour=8, end_hour=18):
    """Return a random datetime on a random day in 2025."""
    # pick a random day in 2025
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 12, 31)
    random_day = start + timedelta(days=random.randint(0, (end-start).days))

    # pick a random hour/minute inside work hours
    hour   = random.randint(start_hour, end_hour-1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return random_day.replace(hour=hour, minute=minute, second=second, microsecond=0)

# ------------------------------------------------------------
# 4. Generate rows
# ------------------------------------------------------------
rows = []
for log_id in range(1, NUM_ROWS + 1):
    # pick a user (same user can appear many times)
    username   = random.choice(USERNAMES)
    user_id    = USERNAMES.index(username) + 100   # simple mapping

    # login time
    login_time = random_workday_timestamp()

    # logout time: 1-8 hours after login (or None for failed logins)
    status = random.choices(STATUSES, weights=[0.92, 0.08], k=1)[0]  # 8% failures
    if status == "SUCCESS":
        duration_hours = random.randint(1, 8)
        logout_time = login_time + timedelta(hours=duration_hours)
    else:
        logout_time = ""   # empty string = no logout

    row = {
        "log_id":       log_id,
        "user_id":      user_id,
        "username":     username,
        "login_time":   login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "logout_time":  logout_time.strftime("%Y-%m-%d %H:%M:%S") if logout_time else "",
        "ip_address":   fake.ipv4(),
        "device_type":  random.choice(DEVICE_TYPES),
        "status":       status,
        "branch_name":  random.choice(BRANCHES),
        "role":         random.choice(ROLES),
    }
    rows.append(row)

# ------------------------------------------------------------
# 5. Write CSV file
# ------------------------------------------------------------
headers = [
    "log_id", "user_id", "username", "login_time", "logout_time",
    "ip_address", "device_type", "status", "branch_name", "role"
]

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()                # first line = column names
    writer.writerows(rows)              # write all rows

print(f"Created {OUTPUT_FILE} with {len(rows)} rows.")