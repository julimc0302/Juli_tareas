import pandas as pd
import numpy as np

path = r"C:\Users\Julia\Downloads\sumer school\python\Tareas2\Juli_tareas\data\metrics\user_metrics.csv"
df = pd.read_csv(path)

print(f"Total rows: {len(df)}")
print("\n--- Language Distribution ---")
langs = df["primary_languages"].dropna().str.split(", ").explode().value_counts()
print(langs.head(10))

print("\n--- Location (City) Distribution ---")
df['city'] = df['location'].fillna('DESCONOCIDO').str.split(',').str[0].str.strip().str.upper()
print(df['city'].value_counts().head(10))

print("\n--- Active Status Distribution ---")
# Check the actual type of 'is_active'
print(f"Type of is_active column: {df['is_active'].dtype}")
print(df['is_active'].value_counts())

print("\n--- Activity by City ---")
active_df = df[df['is_active'].astype(str).str.lower() == 'true']
print(active_df['city'].value_counts().head(10))
