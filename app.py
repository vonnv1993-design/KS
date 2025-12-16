import json
import os
from datetime import date, datetime
from io import BytesIO
from typing import Dict, Any, List, Tuple

import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


# -----------------------------
# Styling
# -----------------------------
def inject_css() -> None:
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

          /* Panels */
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

          @media (max-width: 980px){
            .kv { grid-template-columns: 1fr; }
          }

          /* Sidebar background */
          section[data-testid="stSidebar"] > div {
            background: rgba(0,0,0,0.18);
            border-right: 1px solid rgba(255,255,255,0.08);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Data defaults
# -----------------------------
def default_data() -> Dict[str, Any]:
    return {
        # A1
        "system_name": "",
        "system_code": "",
        "business_group": "",
        "business_owner": "",
        "it_owner": "",
        "vendor_partner": "",
        "system_type": [],
        "aviation_value_role": [],

        # A2
        "business_goal": "",
        "functional_scope": "",
        "user_objects": "",
        "user_count": "",
        "usage_area": [],

        # A3
        "deployment_year": "",
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


ALL_KEYS: List[str] = list(default_data().keys())


def init_state() -> None:
    if "data" not in st.session_state:
        st.session_state.data = default_data()

    if "dirty" not in st.session_state:
        st.session_state.dirty = False

    if "last_saved" not in st.session_state:
        st.session_state.last_saved = None

    if "show_report" not in st.session_state:
        st.session_state.show_report = True

    # Init widget keys (so widgets keep value across reruns)
    for k in ALL_KEYS:
        if k not in st.session_state:
            st.session_state[k] = st.session_state.data.get(k, default_data()[k])


def mark_dirty() -> None:
    st.session_state.dirty = True


def collect_form_data() -> Dict[str, Any]:
    """Collect current widget state into a dict."""
    d = default_data()
    for k in ALL_KEYS:
        d[k] = st.session_state.get(k, d[k])
    return d


def apply_data_to_widgets(d: Dict[str, Any]) -> None:
    """Set widget values from data dict."""
    st.session_state.data = d
    for k in ALL_KEYS:
        st.session_state[k] = d.get(k, default_data()[k])
    st.session_state.dirty = False


def to_json_bytes(d: Dict[str, Any]) -> bytes:
    return json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")


def load_from_uploaded_json(uploaded_file) -> Dict[str, Any]:
    raw = uploaded_file.read()
    obj = json.loads(raw.decode("utf-8"))
    merged = default_data()
    merged.update(obj)
    return merged


# -----------------------------
# Formatting helpers
# -----------------------------
def fmt(v: Any) -> str:
    if v is None:
        return "—"
    s = str(v).strip()
    return s if s else "—"


def fmt_list(v: Any) -> str:
    if not v:
        return "—"
    if isinstance(v, list):
        return ", ".join([str(x) for x in v]) if v else "—"
    return fmt(v)


# -----------------------------
# Report rendering (HTML)
# -----------------------------
def build_report_html(d: Dict[str, Any]) -> str:
    def kv(k: str, v: str) -> str:
        return f"<div class='k'>{k}</div><div class='v'>{v}</div>"

    updated = fmt(d.get("updated_date"))
    updated_by = fmt(d.get("updated_by"))
    version = fmt(d.get("form_version"))

    blocks = []

    blocks.append(
        f"""
        <div class="block">
          <div style="font-weight:700; margin-bottom: 8px;">A. THÔNG TIN TỔNG QUAN, CHUNG</div>
          <div class="kv">
            {kv("Tên hệ thống/phần mềm", fmt(d["system_name"]))}
            {kv("Mã hệ thống (System Code)", fmt(d["system_code"]))}
            {kv("Nhóm nghiệp vụ", fmt(d["business_group"]))}
            {kv("Đơn vị sở hữu nghiệp vụ (Business Owner)", fmt(d["business_owner"]))}
            {kv("Đơn vị quản lý CNTT (IT Owner)", fmt(d["it_owner"]))}
            {kv("Nhà cung cấp / Đối tác", fmt(d["vendor_partner"]))}
            {kv("Loại hệ thống", fmt_list(d["system_type"]))}
            {kv("Vai trò trong chuỗi giá trị hàng không", fmt_list(d["aviation_value_role"]))}

            {kv("Mục tiêu nghiệp vụ chính", fmt(d["business_goal"]))}
            {kv("Phạm vi chức năng", fmt(d["functional_scope"]))}
            {kv("Đối tượng người dùng", fmt(d["user_objects"]))}
            {kv("Số lượng user (hiện tại / dự kiến 3–5 năm)", fmt(d["user_count"]))}
            {kv("Khu vực sử dụng", fmt_list(d["usage_area"]))}

            {kv("Năm triển khai", fmt(d["deployment_year"]))}
            {kv("Tình trạng hiện tại", fmt(d["current_status"]))}
            {kv("Đánh giá mức độ đáp ứng nghiệp vụ (1–5)", fmt(d["biz_fit_score"]))}
            {kv("Kế hoạch 3–5 năm", fmt(d["plan_3_5_years"]))}
          </div>
        </div>
        """
    )

    blocks.append(
        f"""
        <div class="block">
          <div style="font-weight:700; margin-bottom: 8px;">B. THÔNG TIN VỀ HẠ TẦNG (INFRASTRUCTURE)</div>
          <div class="kv">
            {kv("Mô hình hạ tầng", fmt(d["infra_model"]))}
            {kv("Vị trí DC/Cloud Region", fmt(d["dc_region"]))}
            {kv("Nhà cung cấp hạ tầng (AWS/Azure/GCP/IDC…)", fmt(d["infra_provider"]))}

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
        """
    )

    blocks.append(
        f"""
        <div class="block">
          <div style="font-weight:700; margin-bottom: 8px;">C. THÔNG TIN VỀ DỮ LIỆU (DATA)</div>
          <div class="kv">
            {kv("Dữ liệu nghiệp vụ chính (liệt kê 5–10)", fmt(d["main_business_data"]))}
            {kv("Dữ liệu cá nhân (PII)", fmt(d["pii"]))}
            {kv("Dữ liệu nhạy cảm / an ninh hàng không", fmt(d["sensitive_aviation"]))}
            {kv("Dữ liệu tài chính / thanh toán", fmt(d["finance_payment"]))}

            {kv("Nguồn dữ liệu (Source of Truth)", fmt(d["source_of_truth"]))}
            {kv("Định dạng dữ liệu (Structured / Semi / Unstructured)", fmt(d["data_format"]))}
            {kv("Dung lượng dữ liệu (hiện tại / tăng trưởng năm)", fmt(d["data_size_growth"]))}
            {kv("Chính sách lưu trữ & xóa dữ liệu", fmt(d["retention_policy"]))}
            {kv("Chất lượng dữ liệu (Đầy đủ / Chính xác / Kịp thời)", fmt(d["data_quality"]))}

            {kv("Có cung cấp dữ liệu cho BI/AI không?", fmt(d["provide_bi_ai"]))
