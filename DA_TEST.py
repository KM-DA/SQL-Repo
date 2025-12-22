import pandas as pd
import numpy as np

np.random.seed(42)

N_USERS = 2000
START_DATE = "2025-01-01"

# -----------------------
# users
# -----------------------
users = pd.DataFrame({
    "user_id": [f"U{str(i).zfill(5)}" for i in range(N_USERS)],
    "signup_date": pd.to_datetime(START_DATE) + pd.to_timedelta(
        np.random.randint(0, 90, size=N_USERS), unit="D"
    ),
    "group_flag": np.random.choice(["A", "B"], size=N_USERS, p=[0.5, 0.5]),
    "channel": np.random.choice(["API", "BSP", "WEB", "MOB"], size=N_USERS)
})

users["cohort_month"] = users["signup_date"].dt.to_period("M").astype(str)

# -----------------------
# events
# -----------------------
event_types = ["search", "fare_click", "booking_start", "purchase"]

events = []
for _, row in users.iterrows():
    n_events = np.random.randint(5, 20)
    for _ in range(n_events):
        events.append({
            "user_id": row["user_id"],
            "event_date": row["signup_date"] + pd.to_timedelta(
                np.random.randint(0, 30), unit="D"
            ),
            "event_type": np.random.choice(event_types, p=[0.5, 0.25, 0.15, 0.10]),
            "channel": row["channel"]
        })

events = pd.DataFrame(events)

# -----------------------
# transactions
# -----------------------
buyers = users.sample(frac=0.25, random_state=42)

transactions = pd.DataFrame({
    "trx_id": [f"T{str(i).zfill(6)}" for i in range(len(buyers))],
    "user_id": buyers["user_id"].values,
    "trx_date": buyers["signup_date"] + pd.to_timedelta(
        np.random.randint(5, 35, size=len(buyers)), unit="D"
    ),
    "amount": np.random.lognormal(mean=10.5, sigma=0.5, size=len(buyers)).astype(int)
})

# -----------------------
# save
# -----------------------
users.to_csv("data/users.csv", index=False)
events.to_csv("data/events.csv", index=False)
transactions.to_csv("data/transactions.csv", index=False)

print("Synthetic data generated.")