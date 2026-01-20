from google.cloud import bigquery
import pandas as pd

# クライアントの初期化
client = bigquery.Client(project="propane-zephyr-478723-n2")

# データを取得
sql = "SELECT * FROM `sample_dataset.advanced500_sample_customers` LIMIT 10"
df = client.query(sql).to_dataframe()

# 表示
df