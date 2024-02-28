# app_streamlit.py
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

FASTAPI_ENDPOINT = "http://fastapi:8000/get_voltage_data/"

response = requests.get(FASTAPI_ENDPOINT)
data = response.json()

df = pd.DataFrame(data)

# ตรวจสอบรูปแบบข้อมูล timestamp และแปลงถ้าจำเป็น
df['timestamp'] = pd.to_datetime(df['timestamp'])

# คำนวณค่าพลังงาน (วัตต์) = โวลต์ x แอมแปร์
df['power_watt'] = df['voltage'] * df['amp']

# สมมติว่าอัตราค่าไฟฟ้าคือ 4 บาทต่อ kWh
electricity_rate = 4  # บาทต่อ kWh

# คำนวณค่าไฟฟ้า (บาท) = (พลังงานในหน่วยวัตต์ x ชั่วโมง) / 1000 * อัตราค่าไฟฟ้า
# สมมติว่าข้อมูลที่คุณมีครอบคลุมช่วงเวลา 1 ชั่วโมง
df['electricity_cost'] = (df['power_watt'] * 1) / 1000 * electricity_rate

# แสดงข้อมูลในตาราง
st.write("ข้อมูลกระแสไฟ, แรงดันไฟ, ค่าพลังงาน, และค่าใช้จ่ายของไฟฟ้า (บาท):")
st.dataframe(df)

# สร้างกราฟแสดงกระแสไฟ
st.write("กราฟแสดงกระแสไฟ:")
fig_amp = px.line(df, x='timestamp', y='amp', title='กราฟแสดงกระแสไฟ')
st.plotly_chart(fig_amp)

# สร้างกราฟแสดงแรงดันไฟ
st.write("กราฟแสดงแรงดันไฟ:")
fig_voltage = px.line(df, x='timestamp', y='voltage', title='กราฟแสดงแรงดันไฟ')
st.plotly_chart(fig_voltage)

# สร้างกราฟแสดงค่าพลังงาน
st.write("กราฟแสดงค่าพลังงาน (วัตต์):")
fig_power = px.line(df, x='timestamp', y='power_watt', title='กราฟแสดงค่าพลังงาน')
st.plotly_chart(fig_power)

# สร้างกราฟแสดงค่าใช้จ่ายของไฟฟ้า (บาท)
st.write("กราฟแสดงค่าใช้จ่ายของไฟฟ้า (บาท):")
fig_cost = px.line(df, x='timestamp', y='electricity_cost', title='กราฟแสดงค่าใช้จ่ายของไฟฟ้า (บาท)')
st.plotly_chart(fig_cost)
