import json
import sqlite3
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st


DB_PATH = "it_survey.db"
FORM_VERSION = "v1.0"


# ----------------------------
# Database helpers
# ----------------------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS survey_responses (
            system_code TEXT PRIMARY KEY,
            system_name TEXT,
            business_group TEXT,
            updated_by TEXT,
            updated_at TEXT,
            form_version TEXT,
            payload_json TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def upsert_response(
    system_code: str,
    system_name: str,
    business_group: str,
    updated_by: str,
    payload: dict,
):
    conn = get_conn()
    cur = conn.cursor()

    updated_at = datetime.now().isoformat(timespec="seconds")
    payload_json = json.dumps(payload, ensure_ascii=False)

    # Upsert theo system_code
    cur.execute(
        """
        INSERT INTO survey_responses(system_code, system_name, business_group, updated_by, updated_at, form_version, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(system_code) DO UPDATE SET
            system_name=excluded.system_name,
            business_group=excluded.business_group,
            updated_by=excluded.updated_by,
            updated_at=excluded.updated_at,
            form_version=excluded.form_version,
            payload_json=excluded.payload_json
        """,
        (system_code, system_name, business_group, updated_by, updated_at, FORM_VERSION, payload_json),
    )
    conn.commit()
    conn.close()


def get_response_by_code(system_code: str) -> Optional[dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT payload_json FROM survey_responses WHERE system_code = ?", (system_code,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    try:
        return json.loads(row[0]) if row[0] else {}
    except json.JSONDecodeError:
        return {}


def load_all_responses() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM survey_responses ORDER BY updated_at DESC", conn)
    conn.close()
    return df


def delete_by_code(system_code: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM survey_responses WHERE system_code = ?", (system_code,))
    conn.commit()
    conn.close()


# ----------------------------
# Flatten JSON for export
# ----------------------------
def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            # List -> join string for Excel
            if isinstance(v, list):
                v = ", ".join([str(x) for x in v])
            items.append((new_key, v))
    return dict(items)


def build_export_excel(raw_df: pd.DataFrame) -> bytes:
    rows = []
    for _, r in raw_df.iterrows():
        payload = {}
        try:
            payload = json.loads(r["payload_json"]) if r["payload_json"] else {}
        except json.JSONDecodeError:
            payload = {}

        flat = flatten_dict(payload)
        flat.update(
            {
                "meta.system_code": r.get("system_code"),
                "meta.system_name": r.get("system_name"),
                "meta.business_group": r.get("business_group"),
                "meta.updated_by": r.get("updated_by"),
                "meta.updated_at": r.get("updated_at"),
                "meta.form_version": r.get("form_version"),
            }
        )
        rows.append(flat)

    export_df = pd.DataFrame(rows)

    def vc(col: str) -> pd.DataFrame:
        if col not in export_df.columns:
            return pd.DataFrame({"value": [], "count": []})
        s = export_df[col].fillna("N/A").astype(str)
        return s.value_counts().reset_index().rename(columns={"index": "value", "count": "count"})

    summary_blocks = {
        "System Type (A1)": vc("A1.loai_he_thong"),
        "Value Chain Role (A1)": vc("A1.vai_tro"),
        "Deployment Model (B1)": vc("B1.mo_hinh_ha_tang"),
        "Lifecycle Plan 3-5y (A3)": vc("A3.ke_hoach_3_5_nam"),
        "Priority (F)": vc("F.do_uu_tien"),
        "Has PII (C1)": vc("C1.pii"),
        "Realtime Data (C3)": vc("C3.realtime"),
    }

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, sheet_name="RawData", index=False)
        for sheet, sdf in summary_blocks.items():
            sdf.to_excel(writer, sheet_name=sheet[:31], index=False)

    return output.getvalue()


# ----------------------------
# Session-state helpers
# ----------------------------
def set_if_absent(key: str, value: Any):
    if key not in st.session_state:
        st.session_state[key] = value


def clear_form():
    # Xóa các key thuộc form (A..G + meta)
    keys_to_delete = [k for k in st.session_state.keys() if k.startswith(("A", "B", "C", "D", "E", "F", "G"))]
    for k in keys_to_delete:
        del st.session_state[k]


def payload_to_session_state(payload: dict):
    """
    Load payload JSON -> st.session_state để prefill form.
    Payload cấu trúc { "A1": {...}, "A2": {...}, ... }
    """
    # Flatten payload into "A1.xxx" keys
    for section, section_obj in payload.items():
        if isinstance(section_obj, dict):
            for field, value in section_obj.items():
                st.session_state[f"{section}.{field}"] = value
        else:
            st.session_state[str(section)] = section_obj


def get_form_payload() -> Dict[str, Dict[str, Any]]:
    """
    Gom toàn bộ dữ liệu từ st.session_state theo format payload:
    {
      "A1": {...},
      "A2": {...},
      ...
      "G":  {...}
    }
    """
    payload: Dict[str, Dict[str, Any]] = {}
    for key, value in st.session_state.items():
        # chỉ lấy key dạng "A1.xxx"...
        if "." not in key:
            continue
        section, field = key.split(".", 1)
        if section[0] not in list("ABCDEFG"):
            continue
        payload.setdefault(section, {})
        payload[section][field] = value
    return payload


# ----------------------------
# UI Sections A-G
# ----------------------------
def ui_section_A():
    st.subheader("A. THÔNG TIN TỔNG QUAN, CHUNG")

    st.markdown("### A1. Thông tin định danh hệ thống")
    system_name = st.text_input("Tên hệ thống/phần mềm", key="A1.system_name")
    system_code = st.text_input("Mã hệ thống (System Code)", key="A1.system_code")

    business_group = st.selectbox(
        "Nhóm nghiệp vụ",
        [
            "Khai thác bay",
            "Bán – Thương mại",
            "Khách hàng",
            "Bảo dưỡng",
            "Tài chính",
            "Nhân sự",
            "An toàn – An ninh",
            "Khác",
        ],
        key="A1.business_group",
    )
    st.text_input("Đơn vị sở hữu nghiệp vụ (Business Owner)", key="A1.business_owner")
    st.text_input("Đơn vị quản lý CNTT (IT Owner)", key="A1.it_owner")
    st.text_input("Nhà cung cấp / Đối tác", key="A1.vendor")

    st.multiselect("Loại hệ thống", ["COTS", "SaaS", "In-house", "Outsource", "Legacy"], key="A1.loai_he_thong")
    st.multiselect("Vai trò trong chuỗi giá trị hàng không", ["Core", "Support", "Analytics", "Compliance"], key="A1.vai_tro")

    st.markdown("### A2. Mục tiêu & phạm vi")
    st.text_area("Mục tiêu nghiệp vụ chính", key="A2.muc_tieu")
    st.text_area("Phạm vi chức năng", key="A2.pham_vi")
    st.text_input("Đối tượng người dùng", key="A2.doi_tuong")
    st.number_input("Số lượng user (hiện tại)", min_value=0, step=1, key="A2.users_now")
    st.number_input("Số lượng user (dự kiến 3–5 năm)", min_value=0, step=1, key="A2.users_future")
    st.multiselect("Khu vực sử dụng", ["Nội địa", "Quốc tế", "Toàn mạng"], key="A2.khu_vuc")

    st.markdown("### A3. Tình trạng & vòng đời")
    st.number_input("Năm triển khai", min_value=1970, max_value=2100, step=1, key="A3.nam_trien_khai")
    st.selectbox("Tình trạng hiện tại", ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"], key="A3.tinh_trang")
    st.slider("Đánh giá mức độ đáp ứng nghiệp vụ (1–5)", 1, 5, 3, key="A3.dap_ung")
    st.selectbox("Kế hoạch 3–5 năm", ["Giữ nguyên", "Nâng cấp", "Thay thế", "Hợp nhất"], key="A3.ke_hoach_3_5_nam")

    return system_code, system_name, business_group


def ui_section_B():
    st.subheader("B. THÔNG TIN VỀ HẠ TẦNG (INFRASTRUCTURE)")

    st.markdown("### B1. Mô hình triển khai")
    st.selectbox("Mô hình hạ tầng", ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"], key="B1.mo_hinh_ha_tang")
    st.text_input("Vị trí DC/Cloud Region", key="B1.vi_tri")
    st.text_input("Nhà cung cấp hạ tầng (AWS/Azure/GCP/IDC…)", key="B1.nha_cung_cap")

    st.markdown("### B2. Tài nguyên hạ tầng")
    st.text_input("Máy chủ (VM/Physical)", key="B2.may_chu")
    st.text_input("Hệ điều hành", key="B2.he_dieu_hanh")
    st.text_input("CPU / RAM / Storage", key="B2.cpu_ram_storage")
    st.text_input("Database Engine", key="B2.db_engine")
    st.text_input("Middleware", key="B2.middleware")
    st.text_input("Network (LAN/WAN/MPLS/VPN)", key="B2.network")

    st.markdown("### B3. Tính sẵn sàng & an toàn")
    st.text_input("SLA (% uptime)", key="B3.sla")
    st.selectbox("HA/DR", ["Active-Active", "Active-Passive", "None"], key="B3.ha_dr")
    st.text_input("RPO", key="B3.rpo")
    st.text_input("RTO", key="B3.rto")
    st.selectbox("Sao lưu dữ liệu", ["Hàng ngày", "Thời gian thực"], key="B3.sao_luu")
    st.multiselect("Tuân thủ tiêu chuẩn", ["ISO 27001", "PCI DSS", "ICAO", "IATA", "An ninh HK"], key="B3.tuan_thu")


def ui_section_C():
    st.subheader("C. THÔNG TIN VỀ DỮ LIỆU (DATA)")

    st.markdown("### C1. Loại dữ liệu")
    st.text_area("Dữ liệu nghiệp vụ chính", key="C1.du_lieu_nghiep_vu")
    st.selectbox("Dữ liệu cá nhân (PII)", ["Có", "Không"], key="C1.pii")
    st.text_input("Dữ liệu nhạy cảm / an ninh hàng không", key="C1.nhay_cam")
    st.text_input("Dữ liệu tài chính / thanh toán", key="C1.tai_chinh")

    st.markdown("### C2. Quản lý & chất lượng dữ liệu")
    st.text_input("Nguồn dữ liệu (Source of Truth)", key="C2.source_of_truth")
    st.selectbox("Định dạng dữ liệu", ["Structured", "Semi", "Unstructured"], key="C2.dinh_dang")
    st.text_input("Dung lượng dữ liệu (hiện tại / tăng trưởng năm)", key="C2.dung_luong")
    st.text_input("Chính sách lưu trữ & xóa dữ liệu", key="C2.retention")
    st.multiselect("Chất lượng dữ liệu", ["Đầy đủ", "Chính xác", "Kịp thời"], key="C2.quality")

    st.markdown("### C3. Khai thác & phân tích")
    st.selectbox("Có cung cấp dữ liệu cho BI/AI không?", ["Có", "Không"], key="C3.bi_ai")
    st.text_input("Kết nối Data Warehouse / Data Lake", key="C3.dwh_datalake")
    st.text_input("Tần suất đồng bộ dữ liệu", key="C3.tan_suat")
    st.selectbox("Dữ liệu thời gian thực (Real-time)", ["Có", "Không"], key="C3.realtime")


def ui_section_D():
    st.subheader("D. THÔNG TIN VỀ CÔNG NGHỆ TÍCH HỢP / CHIA SẺ")

    st.markdown("### D1. Tích hợp hệ thống")
    st.text_area("Các hệ thống liên quan (PSS, DCS, MRO, CRM, ERP, Contact Center…)", key="D1.he_thong_lien_quan")
    st.selectbox("Vai trò", ["Gửi", "Nhận", "Hai chiều"], key="D1.vai_tro")
    st.multiselect("Hình thức tích hợp", ["API", "ESB", "Message Queue", "File", "Manual"], key="D1.hinh_thuc")

    st.markdown("### D2. Chuẩn & giao thức")
    st.multiselect("Chuẩn dữ liệu", ["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON"], key="D2.chuan_du_lieu")
    st.multiselect("Giao thức", ["REST", "SOAP", "MQ", "SFTP"], key="D2.giao_thuc")
    st.selectbox("Tần suất tích hợp", ["Real-time", "Near real-time", "Batch"], key="D2.tan_suat")

    st.markdown("### D3. Quản trị tích hợp")
    st.selectbox("Có API Gateway không?", ["Có", "Không"], key="D3.api_gateway")
    st.selectbox("Có logging / monitoring không?", ["Có", "Không"], key="D3.logging_monitoring")
    st.text_input("Quản lý version API", key="D3.versioning")
    st.selectbox("Mức độ phụ thuộc hệ thống khác", ["Low", "Medium", "High"], key="D3.phu_thuoc")


def ui_section_E():
    st.subheader("E. THÔNG TIN AN TOÀN – TUÂN THỦ (KHUYẾN NGHỊ)")

    st.multiselect("Phân quyền truy cập", ["RBAC", "ABAC", "Khác"], key="E.phan_quyen")
    st.multiselect("Xác thực", ["SSO", "MFA"], key="E.xac_thuc")
    st.multiselect("Mã hóa dữ liệu", ["At-rest", "In-transit"], key="E.ma_hoa")

    st.multiselect(
        "Tuân thủ pháp lý",
        ["GDPR", "Luật ATTT VN", "ICAO Annex 17", "Khác"],
        key="
