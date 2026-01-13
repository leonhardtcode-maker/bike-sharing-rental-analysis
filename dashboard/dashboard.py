import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# FIRMAN AJI 2024 
# url data = https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data

# ---LOAD CSV FILE---
cwd = os.path.dirname(__file__)

hour_df = pd.read_csv(os.path.join(cwd,'hour.csv'))
day_df = pd.read_csv(os.path.join(cwd,'day.csv'))


# --- HOUR_DF---
# CONVERTING COLUMN DATA TYPE
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['season'] = hour_df.season.astype('category')
hour_df['weathersit'] = hour_df.weathersit.astype('category')

# Konversi nilai untuk kolom 'season' : 1:Winter, 2:Spring, 3:Summer, 4:Fall
hour_df.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)

# Konversi nilai untuk kolom 'weathersit' : 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
hour_df.weathersit.replace((1,2,3,4), ('Clear','Misty','Light_RainSnow','Heavy_RainSnow'), inplace=True)

delta_color='inverse'
hour_df.rename(columns={
    "dteday" : "date",
    "hr": "hour",
    "weathersit" : "weather",
    "cnt" : "total_count"}, inplace=True
)


# --- DAY_DF---
# CONVERTING COLUMN DATA TYPE
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df.season.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

# Konversi nilai untuk kolom 'season' : 1:Winter, 2:Spring, 3:Summer, 4:Fall
day_df.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)

# Konversi nilai untuk kolom 'weathersit' : 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
day_df.weathersit.replace((1,2,3,4), ('Clear','Misty','Light_RainSnow','Heavy_RainSnow'), inplace=True)

# Renam beberapa kolom agar lebih mudah dimengerti
day_df.rename(columns={
    "dteday" : "date",
    "weathersit" : "weather",
    "cnt" : "total_count"}, inplace=True
)


# MEMBUAT DATA MONTHLY UNTUK SETIAP TAHUNNYA
# DATA FRAME DI FILTER BERDASARKAN TAHUN
day_2011_df = day_df.loc[ (day_df['date'].dt.year == 2011) ]
day_2012_df = day_df.loc[ (day_df['date'].dt.year == 2012) ]

# --- HELPER FUNCTION ---

# monthly_2011() bertanggung jawab untuk menghasilkan monthly_2021_df
def monthly_2011(df):
    monthly_2011_df = df.resample(rule='M', on='date').agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
    })
    monthly_2011_df.index = monthly_2011_df.index.strftime('%B')
    monthly_2011_df = monthly_2011_df.reset_index()
    return monthly_2011_df

# monthly_2012() bertanggung jawab untuk menghasilkan monthly_2012_df
def monthly_2012(df):
    monthly_2012_df = df.resample(rule='M', on='date').agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
    })
    monthly_2012_df.index = monthly_2012_df.index.strftime('%B')
    monthly_2012_df = monthly_2012_df.reset_index()
    return monthly_2012_df

# hour_count() bertanggung jawab untuk menghasilkan hour_count_df
def hour_count(df):
    hour_count_df = df.groupby(by="hour").agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
    })
    hour_count_df = hour_count_df.reset_index()
    return hour_count_df

# season_count() bertanggung jawab untuk menghasilkan season_df
def season_count(df):
    season_df = df.groupby(by=["season"]).agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
    })
    season_df = season_df.reset_index()
    return season_df

# weather_count() bertanggung jawab untuk menghasilkan weather_df
def weather_count(df):
    weather_df = df.groupby(by=["weather"]).agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
    })
    weather_df = weather_df.reset_index()
    return weather_df

# DataFrame yang telah difilter inilah yang digunakan untuk menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data. 
# Proses ini tentunya dilakukan dengan memanggil helper function yang telah kita buat sebelumnya.
monthly_2011_df = monthly_2011(day_2011_df)
monthly_2012_df = monthly_2012(day_2012_df)
hour_count_df = hour_count(hour_df)
season_df = season_count(day_df)
weather_df = weather_count(day_df)

# HEADER
st.header(':sparkles: Bike Sharing Dataset Dashboard :sparkles:')

# ---Pertanaan 1---
st.subheader('Pertanyaan 1 : How are the number of users each year, is there an increase or decrease?')
# ---MONTHLY 2011---
st.write("""### Tahun 2011""")

col1, col2 = st.columns(2)
 
with col1:
    min_users_2011 = monthly_2011_df.loc[monthly_2011_df['total_count']. idxmin()]
    min_users_2011 = min_users_2011['date']
    st.metric("Lowest users", value=min_users_2011, delta=int(monthly_2011_df['total_count'].min()), delta_color='inverse')
 
with col2:
    min_users_2011 = monthly_2011_df['total_count'].mean() 
    st.metric("Users per Month", value=int(min_users_2011))

# MONTHLY VISUAL 2011
fig, ax = plt.subplots(figsize=(40, 30))
colors = ["#D3D3D3"]
sns.lineplot(
    y="total_count", 
    x="date",
    data=monthly_2011_df,
    marker='o',
    markersize=30,
    linewidth=8,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Users 2011", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set(ylim=0)
st.pyplot(fig)


# ---MONTHLY 2012---
st.write("""### Tahun 2012""")
col1, col2 = st.columns(2)
 
with col1:
    min_users_2012 = monthly_2012_df.loc[monthly_2012_df['total_count']. idxmin()]
    min_users_2012 = min_users_2012['date']
    st.metric("Lowest Month users", value=min_users_2012, delta=int(monthly_2012_df['total_count'].min()), delta_color='inverse')
 
with col2:
    max_users_2012 = monthly_2012_df['total_count'].mean()
    st.metric("Users per Month", value=int(max_users_2012))

# MONTHLY VISUAL 2012
fig, ax = plt.subplots(figsize=(40, 30))
colors = ["#D3D3D3"]
sns.lineplot(
    y="total_count", 
    x="date",
    data=monthly_2012_df,
    marker='o',
    markersize=30, 
    linewidth=8,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Users 2012", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set(ylim=0)
st.pyplot(fig)

# ---PERTANYAAN 2---
st.subheader('Pertanyaan 2 : Factors that affecting the number of users')

# ---HOUR VISUAL---
fig, ax = plt.subplots(figsize=(40, 30))

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3",
            "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3","#90CAF9","#90CAF9","#D3D3D3"]

sns.barplot(
    y="total_count", 
    x="hour",
    data=hour_count_df,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Users by Hour", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set(ylim=0)
st.pyplot(fig)
 
 # ---SEASON VISUAL---
fig, ax = plt.subplots(figsize=(40, 30))

colors = ["#D3D3D3","#D3D3D3", "#90CAF9", "#D3D3D3"]

sns.barplot(
    y="total_count", 
    x="season",
    data=season_df,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Users based on Seasons", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set(ylim=0)
st.pyplot(fig)

# ---WEATHER VISUAL---
fig, ax = plt.subplots(figsize=(40, 30))

colors = ["#90CAF9", "#D3D3D3","#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="total_count", 
    x="weather",
    data=weather_df,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Users based on Weathers", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set(ylim=0)
st.pyplot(fig)

# CAPTION
st.caption(":blue[Firman Aji] 2024 emojis :sunglasses:")
