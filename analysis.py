from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"

DATA_DIR.mkdir(exist_ok=True)
VISUALS_DIR.mkdir(exist_ok=True)


print("=" * 60)
print("GENERATING BANKING DATA")
print("=" * 60)


N_TRANSACTIONS = 20000
N_CUSTOMERS = 3000


customers = pd.DataFrame({
    "customer_id": range(1, N_CUSTOMERS + 1),

    "age": np.random.randint(
        18,
        75,
        N_CUSTOMERS
    ),

    "region": np.random.choice(
        [
            "North",
            "South",
            "East",
            "West",
            "Central"
        ],
        N_CUSTOMERS
    ),

    "customer_type": np.random.choice(
        [
            "Standard",
            "Premium"
        ],
        N_CUSTOMERS,
        p=[0.75, 0.25]
    )
})


categories = [
    "Groceries",
    "Restaurants",
    "Travel",
    "Electronics",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Clothing"
]


transaction_dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    periods=N_TRANSACTIONS
)


transactions = pd.DataFrame({

    "transaction_id":
        range(1, N_TRANSACTIONS + 1),

    "customer_id":
        np.random.randint(
            1,
            N_CUSTOMERS + 1,
            N_TRANSACTIONS
        ),

    "transaction_date":
        transaction_dates,

    "category":
        np.random.choice(
            categories,
            N_TRANSACTIONS
        ),

    "amount":
        np.round(
            np.random.lognormal(
                mean=3.7,
                sigma=1.0,
                size=N_TRANSACTIONS
            ),
            2
        ),

    "payment_method":
        np.random.choice(
            [
                "Card",
                "Bank Transfer",
                "Online"
            ],
            N_TRANSACTIONS,
            p=[0.60, 0.25, 0.15]
        )
})


transactions["is_fraud"] = 0


# Random fraud transactions
fraud_indices = np.random.choice(
    transactions.index,
    size=int(N_TRANSACTIONS * 0.015),
    replace=False
)

transactions.loc[
    fraud_indices,
    "is_fraud"
] = 1

transactions.loc[
    fraud_indices,
    "amount"
] *= np.random.uniform(
    3,
    8,
    len(fraud_indices)
)


transactions["amount"] = transactions[
    "amount"
].round(2)



customers.to_csv(
    DATA_DIR / "customers.csv",
    index=False
)

transactions.to_csv(
    DATA_DIR / "transactions.csv",
    index=False
)


print(
    f"Customers: {len(customers)}"
)

print(
    f"Transactions: {len(transactions)}"
)



print("\n")
print("=" * 60)
print("DATA QUALITY")
print("=" * 60)


print("\nMissing values:")

print(
    transactions.isna().sum()
)


print("\nDuplicate transactions:")

print(
    transactions.duplicated().sum()
)


transactions = transactions.drop_duplicates()


df = transactions.merge(
    customers,
    on="customer_id",
    how="left"
)



total_transactions = (
    df["transaction_id"].nunique()
)

total_amount = (
    df["amount"].sum()
)

average_transaction = (
    df["amount"].mean()
)

unique_customers = (
    df["customer_id"].nunique()
)

fraud_transactions = (
    df["is_fraud"].sum()
)

fraud_amount = (
    df.loc[
        df["is_fraud"] == 1,
        "amount"
    ].sum()
)


fraud_rate = (
    fraud_transactions
    /
    total_transactions
    *
    100
)


print("\n")
print("=" * 60)
print("BANKING KPIs")
print("=" * 60)


print(
    f"Total transactions: "
    f"{total_transactions:,}"
)

print(
    f"Total transaction volume: "
    f"${total_amount:,.2f}"
)

print(
    f"Average transaction: "
    f"${average_transaction:,.2f}"
)

print(
    f"Unique customers: "
    f"{unique_customers:,}"
)

print(
    f"Fraud transactions: "
    f"{fraud_transactions:,}"
)

print(
    f"Fraud rate: "
    f"{fraud_rate:.2f}%"
)

print(
    f"Fraud transaction volume: "
    f"${fraud_amount:,.2f}"
)



df["month"] = (
    df["transaction_date"]
    .dt.to_period("M")
    .astype(str)
)


monthly = (
    df.groupby("month")
    .agg(
        transactions=(
            "transaction_id",
            "count"
        ),

        total_amount=(
            "amount",
            "sum"
        ),

        average_amount=(
            "amount",
            "mean"
        )
    )
    .reset_index()
)


print("\n")
print("=" * 60)
print("MONTHLY ANALYSIS")
print("=" * 60)

print(
    monthly.to_string(
        index=False
    )
)



category_analysis = (
    df.groupby("category")
    .agg(
        transactions=(
            "transaction_id",
            "count"
        ),

        total_amount=(
            "amount",
            "sum"
        ),

        average_amount=(
            "amount",
            "mean"
        ),

        fraud_count=(
            "is_fraud",
            "sum"
        )
    )
    .sort_values(
        "total_amount",
        ascending=False
    )
)


print("\n")
print("=" * 60)
print("CATEGORY ANALYSIS")
print("=" * 60)

print(
    category_analysis
)


regional = (
    df.groupby("region")
    .agg(
        customers=(
            "customer_id",
            "nunique"
        ),

        transactions=(
            "transaction_id",
            "count"
        ),

        total_amount=(
            "amount",
            "sum"
        ),

        average_amount=(
            "amount",
            "mean"
        )
    )
    .sort_values(
        "total_amount",
        ascending=False
    )
)


print("\n")
print("=" * 60)
print("REGIONAL ANALYSIS")
print("=" * 60)

print(
    regional
)



customer_analysis = (
    df.groupby("customer_id")
    .agg(
        transactions=(
            "transaction_id",
            "count"
        ),

        total_spent=(
            "amount",
            "sum"
        ),

        average_transaction=(
            "amount",
            "mean"
        ),

        fraud_transactions=(
            "is_fraud",
            "sum"
        )
    )
    .sort_values(
        "total_spent",
        ascending=False
    )
)


print("\n")
print("=" * 60)
print("TOP CUSTOMERS")
print("=" * 60)

print(
    customer_analysis.head(10)
)



fraud_summary = (
    df.groupby("is_fraud")
    .agg(
        transactions=(
            "transaction_id",
            "count"
        ),

        total_amount=(
            "amount",
            "sum"
        ),

        average_amount=(
            "amount",
            "mean"
        )
    )
)


print("\n")
print("=" * 60)
print("FRAUD ANALYSIS")
print("=" * 60)

print(
    fraud_summary
)



amount_mean = (
    df["amount"].mean()
)

amount_std = (
    df["amount"].std()
)


df["z_score"] = (
    df["amount"] - amount_mean
) / amount_std


df["amount_anomaly"] = (
    df["z_score"].abs() > 3
).astype(int)


anomalies = df[
    df["amount_anomaly"] == 1
].copy()


print("\n")
print("=" * 60)
print("ANOMALIES")
print("=" * 60)

print(
    f"Anomalous transactions: "
    f"{len(anomalies)}"
)


print(
    anomalies[
        [
            "transaction_id",
            "customer_id",
            "transaction_date",
            "category",
            "amount",
            "is_fraud",
            "z_score"
        ]
    ]
    .sort_values(
        "z_score",
        ascending=False
    )
    .head(10)
)



fraud_by_category = (
    df.groupby("category")
    .agg(
        transactions=(
            "transaction_id",
            "count"
        ),

        fraud_transactions=(
            "is_fraud",
            "sum"
        )
    )
    .reset_index()
)


fraud_by_category[
    "fraud_rate"
] = (
    fraud_by_category[
        "fraud_transactions"
    ]

    /

    fraud_by_category[
        "transactions"
    ]

    * 100
)


fraud_by_category = (
    fraud_by_category
    .sort_values(
        "fraud_rate",
        ascending=False
    )
)


print("\n")
print("=" * 60)
print("FRAUD RATE BY CATEGORY")
print("=" * 60)

print(
    fraud_by_category
)



sns.set_theme(
    style="whitegrid"
)


plt.figure(
    figsize=(12, 6)
)

sns.lineplot(
    data=monthly,
    x="month",
    y="total_amount",
    marker="o"
)

plt.title(
    "Monthly Transaction Volume"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Transaction Volume ($)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    VISUALS_DIR
    / "monthly_transactions.png"
)

plt.close()


plt.figure(
    figsize=(10, 6)
)

sns.barplot(
    data=category_analysis.reset_index(),
    x="category",
    y="total_amount"
)

plt.title(
    "Transaction Volume by Category"
)

plt.xlabel(
    "Category"
)

plt.ylabel(
    "Amount ($)"
)

plt.xticks(
    rotation=30
)

plt.tight_layout()

plt.savefig(
    VISUALS_DIR
    / "category_analysis.png"
)

plt.close()



plt.figure(
    figsize=(9, 6)
)

sns.barplot(
    data=regional.reset_index(),
    x="region",
    y="total_amount"
)

plt.title(
    "Transaction Volume by Region"
)

plt.xlabel(
    "Region"
)

plt.ylabel(
    "Amount ($)"
)

plt.tight_layout()

plt.savefig(
    VISUALS_DIR
    / "regional_analysis.png"
)

plt.close()



plt.figure(
    figsize=(7, 5)
)

sns.countplot(
    data=df,
    x="is_fraud"
)

plt.title(
    "Fraudulent vs Non-Fraudulent Transactions"
)

plt.xlabel(
    "Fraud Flag"
)

plt.ylabel(
    "Transactions"
)

plt.tight_layout()

plt.savefig(
    VISUALS_DIR
    / "fraud_analysis.png"
)

plt.close()


print("\n")
print("=" * 60)
print("CREATING SQLITE DATABASE")
print("=" * 60)


database = (
    BASE_DIR
    / "banking_analytics.db"
)


connection = sqlite3.connect(
    database
)


customers.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)


df.to_sql(
    "transactions",
    connection,
    if_exists="replace",
    index=False
)



query = """

SELECT

    category,

    COUNT(*) AS transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount,

    ROUND(
        AVG(amount),
        2
    ) AS average_transaction

FROM transactions

GROUP BY category

ORDER BY total_amount DESC;

"""


sql_result = pd.read_sql_query(
    query,
    connection
)


print("\n")
print("=" * 60)
print("SQL CATEGORY ANALYSIS")
print("=" * 60)

print(
    sql_result.to_string(
        index=False
    )
)


risk_query = """

SELECT

    customer_id,

    COUNT(*) AS transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_spent,

    SUM(
        CASE
            WHEN is_fraud = 1
            THEN 1
            ELSE 0
        END
    ) AS fraud_transactions

FROM transactions

GROUP BY customer_id

HAVING fraud_transactions > 0

ORDER BY fraud_transactions DESC;

"""


risk_result = pd.read_sql_query(
    risk_query,
    connection
)


print("\n")
print("=" * 60)
print("HIGH-RISK CUSTOMERS")
print("=" * 60)

print(
    risk_result.head(20)
)


best_category = (
    category_analysis
    .index[0]
)

best_region = (
    regional
    .index[0]
)

highest_fraud_category = (
    fraud_by_category
    .iloc[0]["category"]
)


print("\n")
print("=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)


print(
    f"""
1. The largest transaction volume
   comes from the "{best_category}"
   category.

2. The strongest region by transaction
   volume is "{best_region}".

3. The category with the highest
   observed fraud rate is
   "{highest_fraud_category}".

4. Large transactions can be flagged
   using statistical anomaly detection
   based on Z-score.

5. Customers with repeated fraudulent
   transactions should receive additional
   risk monitoring.

6. Fraud monitoring should combine
   transaction amount, customer history,
   transaction frequency and category
   rather than relying on a single metric.
"""
)


connection.close()


print("\n")
print("=" * 60)
print("ANALYSIS COMPLETED")
print("=" * 60)