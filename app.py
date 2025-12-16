# app.py
# Streamlit App – Software System Survey & Reporting

import json
from datetime import date
from typing import Dict, Any, List

import streamlit as st

# -----------------------------
# Styling
# -----------------------------

def inject_css() -> None:
    st.markdown(
        """
        <style>
          .stApp {
            background:
              radial-gradient(900px 500px at 20% 10%, rgba(110,231,255,0.18), transparent 65%),
              radial-gradient(900px 500px at 70% 25%, rgba(167,139,250,0.16), transparent 70%),
              radial-gradient(1000px 700px at 50% 95%, rgba(45,212,191,0.12), transparent 60%),
              linear-gradient(180deg, #070b14, #0b1220);
          }
          .panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
          }
          .report {
            background: #ffffff;
            color: #0b1220;
            border-radius: 14px;
            padding: 18px;
          }
          .kv { display: grid; grid-template-columns: 220px 1fr; gap: 8px 12px; font-size: 12.5px; }
          .k { color: rgba(0,0,0,0.65); }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Default data model
# -----------------------------

def default_data() -> Dict[str, Any]:
    return {
        # A
        "system_name": "",
        "system_code": "",
        "business_group": "",
        "business_owner": "",
        "it_owner": "",
        "vendor_partner": "",
        "system_type": [],
        "aviation_value_role": [],
        "business_goal": "",
        "functional_scope": "",
        "user_objects": "",
        "user_count": "",
        "usage_area": [],
        "deployment_year": "",
        "current_status": "",
        "biz_fit_score": 3,
        "plan_3_5_years": "",
        # B
        "infra_model": "",
        "dc_region": "",
        "infra_provider": "",
        "servers": "",
        "os": "",
        "cpu_ram_storage": "",
        "db_engine": "",
        "middleware": "",
        "network": "",
        "sla_uptime": "",
        "ha_dr": "",
        "rpo_rto": "",
        "backup": [],
        "compliance": [],
        # C
        "main_business_data": "",
        "pii": "",
        "sensitive_aviation": "",
        "finance_payment": "",
        "source_of_truth": "",
        "data_format": "",
        "data_size_growth": "",
        "retention_policy": "",
        "data_quality": "",
        "provide_bi_ai": "",
        "dw_dl_connection": "",
        "sync_frequency": "",
        "realtime_data": "",
        # D
        "related_systems": "",
        "integration_role": "",
        "integration_method": [],
        "data_standards": [],
        "protocols": [],
        "integration_frequency": "",
        "api_gateway": "",
        "logging_monitoring": "",
        "api_versioning": "",
        "dependency_level": "",
        # E
        "rbac": "",
        "auth_methods": [],
        "encryption": "",
        "legal_compliance": [],
        # F
        "digital_strategy_fit": 3,
        "cloud_ai_readiness": "",
        "scalability": "",
        "recommendation": "",
        "priority": "",
        # G
        "updated_by": "",
        "updated_date": str(date.today()),
        "form_version": "1.0",
        "notes": "",
    }

ALL_KEYS: List[str] = list(default_data().keys())

# -----------------------------
# State helpers
# -----------------------------

def init_state():
    if "data" not in st.session_state:
        st.session_state.data = default_data()
    for k in ALL_KEYS:
        if k not in st.session_state:
            st.session_state[k] = st.session_state.data.get(k, "")


def collect_form_data() -> Dict[str, Any]:
    d = default_data()
    for k in ALL_KEYS:
        d[k] = st.session_state.get(k)
    return d

# -----------------------------
# Formatting helpers
# -----------------------------

def fmt(v: Any) -> str:
    if v is None:
        return "—"
    s = str(v).strip()
    return s if s else "—"


def fmt_list(v: Any) -> str:
    if isinstance(v, list) and v:
        return ", ".join(v)
    return "—"

# -----------------------------
# Report HTML
# -----------------------------

def build_report_html(d: Dict[str, Any]) -> str:
    def kv(k, v):
        return f"<div class='k'>{k}</div><div class='v'>{v}</div>"

    return f"""
    <div class='report'>
      <h2>BÁO CÁO KHẢO SÁT HỆ THỐNG PHẦN MỀM</h2>
      <div class='kv'>
        {kv('Tên hệ thống', fmt(d['system_name']))}
        {kv('Mã hệ thống', fmt(d['system_code']))}
        {kv('Đơn vị nghiệp vụ', fmt(d['business_owner']))}
        {kv('Đơn vị CNTT', fmt(d['it_owner']))}
        {kv('Nhà cung cấp', fmt(d['vendor_partner']))}
        {kv('Loại hệ thống', fmt_list(d['system_type']))}
        {kv('Vai trò chuỗi giá trị HK', fmt_list(d['aviation_value_role']))}
        {kv('Mục tiêu nghiệp vụ', fmt(d['business_goal']))}
        {kv('Phạm vi chức năng', fmt(d['functional_scope']))}
        {kv('Hạ tầng', fmt(d['infra_model']))}
        {kv('DB Engine', fmt(d['db_engine']))}
        {kv('Dữ liệu chính', fmt(d['main_business_data']))}
        {kv('PII', fmt(d['pii']))}
        {kv('Tích hợp BI/AI', fmt(d['provide_bi_ai']))}
        {kv('Phương thức tích hợp', fmt_list(d['integration_method']))}
        {kv('Khuyến nghị', fmt(d['recommendation']))}
        {kv('Mức ưu tiên', fmt(d['priority']))}
        {kv('Cập nhật bởi', fmt(d['updated_by']))}
        {kv('Ngày cập nhật', fmt(d['updated_date']))}
      </div>
    </div>
    """

# -----------------------------
# Main App
# -----------------------------

def main():
    st.set_page_config(page_title="Software System Survey", layout="wide")
    inject_css()
    init_state()

    st.title("📋 Khảo sát & Quy hoạch Hệ thống Phần mềm")

    with st.sidebar:
        st.header("Quản lý dữ liệu")
        uploaded = st.file_uploader("Upload JSON", type=["json"])
        if uploaded:
            st.session_state.data = json.load(uploaded)
            for k in ALL_KEYS:
                st.session_state[k] = st.session_state.data.get(k)
            st.success("Đã nạp dữ liệu")

        data = collect_form_data()
        st.download_button(
            "⬇️ Tải JSON",
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="survey_system.json",
            mime="application/json",
        )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("📝 Form khảo sát")
        st.text_input("Tên hệ thống", key="system_name")
        st.text_input("Mã hệ thống", key="system_code")
        st.text_input("Đơn vị nghiệp vụ", key="business_owner")
        st.text_input("Đơn vị CNTT", key="it_owner")
        st.text_input("Nhà cung cấp", key="vendor_partner")
        st.multiselect("Loại hệ thống", ["Core", "Support", "Legacy", "Cloud-native"], key="system_type")
        st.multiselect("Vai trò chuỗi giá trị HK", ["Bán vé", "Khai thác bay", "Bảo dưỡng", "DVHK", "Tài chính"], key="aviation_value_role")
        st.text_area("Mục tiêu nghiệp vụ", key="business_goal")
        st.text_area("Phạm vi chức năng", key="functional_scope")
        st.selectbox("Mô hình hạ tầng", ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"], key="infra_model")
        st.text_input("DB Engine", key="db_engine")
        st.text_area("Dữ liệu nghiệp vụ chính", key="main_business_data")
        st.selectbox("Có PII?", ["Có", "Không"], key="pii")
        st.selectbox("Cung cấp BI/AI?", ["Có", "Không"], key="provide_bi_ai")
        st.multiselect("Phương thức tích hợp", ["API", "File", "ESB", "Message Queue"], key="integration_method")
        st.text_area("Khuyến nghị", key="recommendation")
        st.selectbox("Mức ưu tiên", ["Cao", "Trung bình", "Thấp"], key="priority")
        st.text_input("Cập nhật bởi", key="updated_by")

    with col2:
        st.subheader("📊 Báo cáo tổng hợp")
        report_html = build_report_html(collect_form_data())
        st.markdown(report_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
