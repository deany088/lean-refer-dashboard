Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
pip install streamlit pandas

SyntaxError: invalid syntax
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="LEAN Refer-In Dashboard", layout="wide")

st.title("📊 LEAN Refer-In KPI Dashboard")

# -- Data Entry Section --
st.header("➕ บันทึกข้อมูล Refer-in")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        patient_id = st.text_input("Patient ID")
        start_time = st.time_input("เริ่มรับเคส (เวลา)", value=datetime.now().time())
        accept_time = st.time_input("เวลาตอบรับ", value=datetime.now().time())
        transport_time = st.time_input("เวลาออกจากต้นทาง", value=datetime.now().time())
    with col2:
        smi_complete = st.selectbox("SMI ครบถ้วนหรือไม่?", ["Yes", "No"])
        delay_more_than_2hr = st.selectbox("Delay > 2 ชม.?", ["No", "Yes"])
    
    submitted = st.form_submit_button("บันทึก")

if submitted:
    new_entry = {
        "PatientID": patient_id,
        "StartTime": str(start_time),
        "AcceptTime": str(accept_time),
        "TransportTime": str(transport_time),
        "SMI": smi_complete,
        "Delay2hr": delay_more_than_2hr
    }
    try:
        df = pd.read_csv("refer_data.csv")
    except:
        df = pd.DataFrame(columns=new_entry.keys())

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
...     df.to_csv("refer_data.csv", index=False)
...     st.success("✅ บันทึกข้อมูลเรียบร้อย")
... 
... # -- KPI Section --
... st.header("📈 KPI Summary")
... 
... try:
...     df = pd.read_csv("refer_data.csv")
...     df["StartTime"] = pd.to_datetime(df["StartTime"], format="%H:%M:%S").dt.time
...     df["AcceptTime"] = pd.to_datetime(df["AcceptTime"], format="%H:%M:%S").dt.time
... 
...     def calc_minutes(t1, t2):
...         return (datetime.combine(datetime.today(), t2) - datetime.combine(datetime.today(), t1)).seconds / 60
... 
...     df["CycleTime"] = df.apply(lambda row: calc_minutes(row["StartTime"], row["TransportTime"]), axis=1)
...     df["SLA15min"] = df.apply(lambda row: "Yes" if calc_minutes(row["StartTime"], row["AcceptTime"]) <= 15 else "No", axis=1)
... 
...     total_cases = len(df)
...     avg_cycle_time = round(df["CycleTime"].mean(), 1)
...     sla_percent = round((df["SLA15min"] == "Yes").mean() * 100, 1)
...     smi_percent = round((df["SMI"] == "Yes").mean() * 100, 1)
...     delay_count = (df["Delay2hr"] == "Yes").sum()
... 
...     col1, col2, col3, col4 = st.columns(4)
...     col1.metric("🕒 Avg. Refer-in Time (min)", avg_cycle_time)
...     col2.metric("📩 SLA ≤ 15 min", f"{sla_percent}%")
...     col3.metric("📄 SMI Completeness", f"{smi_percent}%")
...     col4.metric("⚠️ Delay > 2 hr", f"{delay_count} cases")
... 
...     with st.expander("📋 ดูข้อมูลทั้งหมด"):
...         st.dataframe(df)
... 
... except:
...     st.warning("ยังไม่มีข้อมูล refer-in กรุณาบันทึกอย่างน้อย 1 เคสก่อน")
... 
