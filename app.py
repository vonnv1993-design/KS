import json
from datetime import date, datetime
from io import BytesIO

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


# -----------------------------
# UI helpers
# -----------------------------
def inject_css():
    st.markdown(
        """
        <style>
          /* App background gradient */
          .stApp {
            background:
              radial-gradient(900px 500px at 20% 10%, rgba(110,231,255,0.18), transparent 65%),
              radial-gradient(900px 500px at 70% 25%, rgba(167,139,250,0.16), transparent 70%),
              radial-gradient(1000px 700px at 50% 95%, rgba(45,212,191,0.12), transparent 60%),
              linear-gradient(180deg, #070b14, #0b1220);
          }

          /* Cards / panels feel */
          .panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 14px 14px 12px 14px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
            margin-bottom: 12px;
          }

          /* Report card white */
          .report {
            background: #ffffff;
            color: #0b1220;
            border-radius: 14px;
            padding: 18px;
            border: 1px solid rgba(0,0,0,0.08);
          }
          .report h2 { margin: 0 0 8px 0; font-size: 16px; }
          .report .small { color: rgba(0,0,0,0.65); font-size: 12px; margin-bottom: 12px; }
          .report .block { border-top: 1px solid rgba(0,0,0,0.10); padding-top: 10px; margin-top: 10px; }
          .kv { display: grid; grid-template-columns: 220px 1fr; gap: 8px 12px; font-size: 12.5px; align-items: start; }
          .kv .k { color: rgba(0,0,0,0.66); }
          .kv .v { white-space: pre-wrap; }
          @media (max-width: 980px){ .kv { grid-template-columns: 1fr; } }

          /* Make sidebar more panel-like */
          section[data-testid="stSidebar"] > div {
            background: rgba(0,0,0,0.18);
            border-right: 1px solid rgba(255,255,255,0.08);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def panel(title: str, subtitle: str | None = None):
    sub_html = f"<div style='color: rgba(255,255,255,0.70); font-size: 12.5px; line-height: 1.4;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div class="panel">
          <div style="display:flex; justify-content:space-between; gap: 12px; align-items: baseline;">
            <div>
              <div style="font-weight: 700; letter-spacing: .2px; font-size: 14px; margin-bottom: 6px;">{title}</div>
              {sub_html}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Data model
# -----------------------------
def default_data():
    return {
        # A1
        "system_name": "",
        "system_code": "",
        "business_group": "",
        "business_owner": "",
        "it_owner": "",
        "vendor_partner": "",
        "system_type": [],  # COTS/SaaS/In-house/Outsource/Legacy
        "aviation_value_role": [],  # Core/Support/Analytics/Compliance

        # A2
        "business_goal": "",
        "functional_scope": "",
        "user_objects": "",
        "user_count": "",
        "usage_area": [],  # Nội địa/Quốc tế/Toàn mạng

        # A3
        "deployment_year": None,
        "current_status": "",
        "biz_fit_score": 3,
        "plan_3_5_years": "",

        # B1
        "infra_model": "",
        "dc_region": "",
        "infra_provider": "",

        # B2
        "servers": "",
        "os": "",
        "cpu_ram_storage": "",
        "db_engine": "",
        "middleware": "",
        "network": "",

        # B3
        "sla_uptime": "",
        "ha_dr": "",
        "rpo_rto": "",
        "backup": [],
        "compliance": [],

        # C1
        "main_business_data": "",
        "pii": "",
        "sensitive_aviation": "",
        "finance_payment": "",

        # C2
        "source_of_truth": "",
        "data_format": "",
        "data_size_growth": "",
        "retention_policy": "",
        "data_quality": "",

        # C3
        "provide_bi_ai": "",
        "dw_dl_connection": "",
        "sync_frequency": "",
        "realtime_data": "",

        # D1
        "related_systems": "",
        "integration_role": "",
        "integration_method": [],

        # D2
        "data_standards": [],
        "protocols": [],
        "integration_frequency": "",

        # D3
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


def init_state():
    if "data" not in st.session_state:
        st.session_state.data = default_data()
    if "last_saved" not in st.session_state:
        st.session_state.last_saved = None


def to_json_bytes(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")


def load_from_uploaded_json(uploaded_file) -> dict:
    raw = uploaded_file.read()
    obj = json.loads(raw.decode("utf-8"))
    # Merge with defaults to avoid missing keys
    d = default_data()
    d.update(obj)
    return d


# -----------------------------
# Report & PDF
# -----------------------------
def fmt_list(v):
    if not v:
        return "—"
    if isinstance(v, list):
        return ", ".join(v) if v else "—"
    return str(v).strip() if str(v).strip() else "—"


def fmt(v):
    if v is None:
        return "—"
    s = str(v).strip()
    return s if s else "—"


def build_report_html(d: dict) -> str:
    def kv(k, v):
        return f"<div class='k'>{k}</div><div class='v'>{v}</div>"

    blocks = []

    blocks.append(f"""
      <div class="block">
        <div style="font-weight:700; margin-bottom: 8px;">A. THÔNG TIN TỔNG QUAN, CHUNG</div>
        <div class="kv">
          {kv("Tên hệ thống/phần mềm", fmt(d["system_name"]))}
          {kv("Mã hệ thống (System Code)", fmt(d["system_code"]))}
          {kv("Nhóm nghiệp vụ", fmt(d["business_group"]))}
          {kv("Business Owner", fmt(d["business_owner"]))}
          {kv("IT Owner", fmt(d["it_owner"]))}
          {kv("Nhà cung cấp/Đối tác", fmt(d["vendor_partner"]))}
          {kv("Loại hệ thống", fmt_list(d["system_type"]))}
          {kv("Vai trò trong chuỗi giá trị hàng không", fmt_list(d["aviation_value_role"]))}
          {kv("Mục tiêu nghiệp vụ chính", fmt(d["business_goal"]))}
          {kv("Phạm vi chức năng", fmt(d["functional_scope"]))}
          {kv("Đối tượng người dùng", fmt(d["user_objects"]))}
          {kv("Số lượng user (hiện tại / dự kiến 3–5 năm)", fmt(d["user_count"]))}
          {kv("Khu vực sử dụng", fmt_list(d["usage_area"]))}
          {kv("Năm triển khai", fmt(d["deployment_year"]))}
          {kv("Tình trạng hiện tại", fmt(d["current_status"]))}
          {kv("Đánh giá đáp ứng nghiệp vụ (1–5)", fmt(d["biz_fit_score"]))}
          {kv("Kế hoạch 3–5 năm", fmt(d["plan_3_5_years"]))}
        </div>
      </div>
    """)

    blocks.append(f"""
      <div class="block">
        <div style="font-weight:700; margin-bottom: 8px;">B. THÔNG TIN VỀ HẠ TẦNG (INFRASTRUCTURE)</div>
        <div class="kv">
          {kv("Mô hình hạ tầng", fmt(d["infra_model"]))}
          {kv("Vị trí DC/Cloud Region", fmt(d["dc_region"]))}
          {kv("Nhà cung cấp hạ tầng", fmt(d["infra_provider"]))}
          {kv("Máy chủ (VM/Physical)", fmt(d["servers"]))}
          {kv("Hệ điều hành", fmt(d["os"]))}
          {kv("CPU / RAM / Storage", fmt(d["cpu_ram_storage"]))}
          {kv("Database Engine", fmt(d["db_engine"]))}
          {kv("Middleware", fmt(d["middleware"]))}
          {kv("Network (LAN/WAN/MPLS/VPN)", fmt(d["network"]))}
          {kv("SLA (% uptime)", fmt(d["sla_uptime"]))}
          {kv("HA/DR", fmt(d["ha_dr"]))}
          {kv("RPO / RTO", fmt(d["rpo_rto"]))}
          {kv("Sao lưu dữ liệu", fmt_list(d["backup"]))}
          {kv("Tuân thủ tiêu chuẩn", fmt_list(d["compliance"]))}
        </div>
      </div>
    """)

    blocks.append(f"""
      <div class="block">
        <div style="font-weight:700; margin-bottom: 8px;">C. THÔNG TIN VỀ DỮ LIỆU (DATA)</div>
        <div class="kv">
          {kv("Dữ liệu nghiệp vụ chính (5–10 dữ liệu)", fmt(d["main_business_data"]))}
          {kv("Dữ liệu cá nhân (PII)", fmt(d["pii"]))}
          {kv("Dữ liệu nhạy cảm / an ninh hàng không", fmt(d["sensitive_aviation"]))}
          {kv("Dữ liệu tài chính / thanh toán", fmt(d["finance_payment"]))}
          {kv("Source of Truth", fmt(d["source_of_truth"]))}
          {kv("Định dạng dữ liệu", fmt(d["
