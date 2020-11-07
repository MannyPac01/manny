import pandas as pd

df = pd.read_csv('ratings.csv')

df_avg = df.groupby('CLIENT_NUMBER').mean()
df_avg.to_csv('avg_ratings.csv')
