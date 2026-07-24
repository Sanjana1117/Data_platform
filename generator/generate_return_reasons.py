import pandas as pd
from config import Config

OUTPUT = Config.RETURN_REASONS_FILE

reasons = [

    ("Damaged Product","Full"),

    ("Wrong Item Delivered","Full"),

    ("Missing Item","Full"),

    ("Defective Product","Full"),

    ("Quality Issue","Partial"),

    ("Changed Mind","Partial"),

    ("Ordered by Mistake","Partial"),

    ("Late Delivery","Partial"),

    ("Duplicate Order","Full"),

    ("Other","Partial")

]

df = pd.DataFrame(
    reasons,
    columns=[
        "reason",
        "refund_type"
    ]
)

df.insert(
    0,
    "reason_id",
    range(1,len(df)+1)
)

df.to_csv(
    OUTPUT,
    index=False
)

print(df)