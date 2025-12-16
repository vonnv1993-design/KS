import streamlit as st
import json, os
from datetime import datetime

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Vietnam Airlines | Khảo sát CNTT",
    layout="wide"
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "form" not in st.session_state:
    st.session_state.form = {
        "A": {"A1": {}, "A2": {}, "A3": {}},
        "B": {"B1": {}, "B2": {}, "B3": {}},
        "C": {"C1": {}, "C2": {}, "C3": {}},
        "D": {"D1": {}, "D2": {}, "D3": {}},
        "E": {},
        "F": {},
        "G": {}
    }

f = st.session_state.form

# ======================
# BRAND STYLE – VNA
# ======================
st.markdown("""
<style>
body {background-color:#F7F9FC;}
header {visibility:hidden;}
.block-container {padding-top:1.5rem;}
.vna-card {
    background:white;
    border-radius:14px;
    padding:22px;
    border:1px solid #E5EAF1;
    margin-bottom:22px;
}
.stTabs [aria-selected="true"] {
    background-color:#005EB8;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## ✈️ VIETNAM AIRLINES – KHẢO SÁT QUY HOẠCH HỆ THỐNG CNTT")
st.divider()

# ======================
# TABS
# ======================
tabA, tabB, tabC, tabD, tabE, tabF, tabG = st.tabs([
    "A. Thông tin chung",
    "B. Hạ tầng",
    "C. Dữ liệu",
    "D. Tích hợp",
    "E. An toàn – Tuân thủ",
    "F. Đánh giá – Quy hoạch",
    "G. Lưu & Quản lý"
])

# ======================
# TAB A
# ======================
with tabA:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("A1. Thông tin định danh")

    f["A"]["A1"]["system_name"] = st.text_input("Tên hệ thống")
    f["A"]["A1"]["system_code"] = st.text_input("Mã hệ thống")
    f["A"]["A1"]["business_group"] = st.multiselect(
        "Nhóm nghiệp vụ",
        ["Khai thác bay","Thương mại","Dịch vụ","Kỹ thuật","Tài chính","Nhân sự","An toàn – An ninh","Quản lý chung"]
    )
    f["A"]["A1"]["business_owner"] = st.text_input("Đơn vị sở hữu nghiệp vụ")
    f["A"]["A1"]["it_owner"] = st.text_input("Đơn vị quản lý CNTT")
    f["A"]["A1"]["vendor"] = st.text_input("Nhà cung cấp / Đối tác")
    f["A"]["A1"]["system_type"] = st.multiselect(
        "Loại hệ thống",
        ["COTS","SaaS","In-house","Outsource","Legacy"]
    )
    f["A"]["A1"]["value_chain_role"] = st.multiselect(
        "Vai trò chuỗi giá trị",
        ["Core","Support","Analytics","Compliance"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("A2. Mục tiêu & phạm vi")
    f["A"]["A2"]["business_goal"] = st.text_area("Mục tiêu nghiệp vụ")
    f["A"]["A2"]["scope"] = st.text_area("Phạm vi chức năng")
    f["A"]["A2"]["users"] = st.text_input("Đối tượng người dùng")
    f["A"]["A2"]["user_scale"] = st.multiselect(
        "Quy mô người dùng",
        ["<10","10–50","50–100",">100"]
    )
    f["A"]["A2"]["region"] = st.multiselect(
        "Khu vực sử dụng",
        ["Nội địa","Quốc tế","Toàn mạng"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("A3. Tình trạng & vòng đời")
    f["A"]["A3"]["deploy_year"] = st.selectbox("Năm triển khai", list(range(2000,2051)))
    f["A"]["A3"]["status"] = st.radio(
        "Tình trạng hiện tại",
        ["Đang vận hành","Nâng cấp","Thay thế","Dừng"]
    )
    f["A"]["A3"]["business_fit"] = st.slider("Mức độ đáp ứng nghiệp vụ",1,5)
    f["A"]["A3"]["plan_3_5y"] = st.multiselect(
        "Kế hoạch 3–5 năm",
        ["Giữ nguyên","Nâng cấp","Thay thế","Hợp nhất"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB B
# ======================
with tabB:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("B1. Mô hình triển khai")
    f["B"]["B1"]["infra_model"] = st.multiselect(
        "Mô hình hạ tầng",
        ["On-Prem","Private Cloud","Public Cloud","Hybrid"]
    )
    f["B"]["B1"]["dc_region"] = st.text_input("Vị trí DC / Cloud Region")
    f["B"]["B1"]["provider"] = st.multiselect(
        "Nhà cung cấp",
        ["AWS","Azure","Viettel","VNPT","FPT","Khác"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("B2. Tài nguyên hạ tầng")
    f["B"]["B2"]["server_type"] = st.radio("Máy chủ",["VM","Physical"])
    f["B"]["B2"]["os"] = st.text_input("Hệ điều hành")
    f["B"]["B2"]["resource"] = st.text_input("CPU / RAM / Storage")
    f["B"]["B2"]["database"] = st.text_input("Database Engine")
    f["B"]["B2"]["middleware"] = st.text_input("Middleware")
    f["B"]["B2"]["network"] = st.text_input("Network")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("B3. Sẵn sàng & an toàn")
    f["B"]["B3"]["sla"] = st.slider("SLA (%)",90,100)
    f["B"]["B3"]["ha_dr"] = st.multiselect(
        "HA / DR",
        ["Active-Active","Active-Passive","None"]
    )
    f["B"]["B3"]["rpo_rto"] = st.text_input("RPO / RTO")
    f["B"]["B3"]["backup"] = st.multiselect(
        "Sao lưu",
        ["Hàng ngày","Thời gian thực"]
    )
    f["B"]["B3"]["standards"] = st.multiselect(
        "Tuân thủ",
        ["ISO 27001","PCI DSS","ICAO","IATA"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB C
# ======================
with tabC:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("C1. Loại dữ liệu")
    f["C"]["C1"]["pii"] = st.radio("Dữ liệu cá nhân (PII)",["Có","Không"])
    f["C"]["C1"]["sensitive"] = st.radio("Dữ liệu nhạy cảm",["Có","Không"])
    f["C"]["C1"]["finance"] = st.radio("Dữ liệu tài chính",["Có","Không"])
    f["C"]["C1"]["cross_border"] = st.radio("Dữ liệu ra nước ngoài",["Có","Không"])
    f["C"]["C1"]["core_data"] = st.text_area("Dữ liệu nghiệp vụ trọng yếu")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("C2. Quản lý & chất lượng")
    f["C"]["C2"]["source"] = st.text_input("Source of Truth")
    f["C"]["C2"]["format"] = st.multiselect(
        "Định dạng",
        ["Structured","Semi-structured","Unstructured"]
    )
    f["C"]["C2"]["volume"] = st.text_input("Dung lượng / tăng trưởng")
    f["C"]["C2"]["policy"] = st.text_input("Chính sách lưu trữ & xoá")
    f["C"]["C2"]["quality"] = st.multiselect(
        "Chất lượng dữ liệu",
        ["Đầy đủ","Chính xác","Kịp thời"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("C3. Khai thác & phân tích")
    f["C"]["C3"]["bi_ai"] = st.radio("Kết nối BI / AI",["Có","Không"])
    f["C"]["C3"]["dw_dl"] = st.radio("Kết nối DW / DL",["Có","Không"])
    f["C"]["C3"]["sync"] = st.text_input("Tần suất đồng bộ")
    f["C"]["C3"]["realtime"] = st.radio("Dữ liệu realtime",["Có","Không"])
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB D
# ======================
with tabD:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("D1. Tích hợp hệ thống")
    f["D"]["D1"]["systems"] = st.text_area(
        "Danh sách hệ thống tích hợp",
        placeholder="STT | Tên | Vai trò | Hình thức"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("D2. Chuẩn & giao thức")
    f["D"]["D2"]["data_standard"] = st.multiselect(
        "Chuẩn dữ liệu",
        ["IATA NDC","AIDX","EDIFACT","XML","JSON","Khác"]
    )
    f["D"]["D2"]["protocol"] = st.multiselect(
        "Giao thức",
        ["REST","SOAP","MQ","SFTP"]
    )
    f["D"]["D2"]["frequency"] = st.radio(
        "Tần suất",
        ["Real-time","Near real-time","Batch"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("D3. Quản trị tích hợp")
    f["D"]["D3"]["api_gateway"] = st.radio("API Gateway",["Có","Không"])
    f["D"]["D3"]["logging"] = st.radio("Logging / Monitoring",["Có","Không"])
    f["D"]["D3"]["versioning"] = st.radio("Quản lý version API",["Có","Không"])
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB E
# ======================
with tabE:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["E"]["rbac"] = st.text_input("Phân quyền (RBAC)")
    f["E"]["auth"] = st.multiselect("Xác thực",["SSO","MFA","Khác"])
    f["E"]["encryption"] = st.text_input("Mã hoá dữ liệu (At-rest / In-transit)")
    f["E"]["legal"] = st.multiselect(
        "Tuân thủ pháp lý",
        ["GDPR","Luật ATTT VN","ICAO Annex 17","Quy chế ANTT TCTHK"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB F
# ======================
with tabF:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["F"]["strategy_fit"] = st.slider("Phù hợp chiến lược số",1,5)
    f["F"]["cloud_ai_ready"] = st.text_input("Sẵn sàng Cloud / AI")
    f["F"]["scalability"] = st.text_input("Khả năng mở rộng")
    f["F"]["proposal"] = st.radio(
        "Đề xuất",
        ["Giữ nguyên","Nâng cấp","Hợp nhất","Thay thế"]
    )
    f["F"]["priority"] = st.radio(
        "Độ ưu tiên",
        ["High","Medium","Low"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB G
# ======================
with tabG:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["G"]["updated_by"] = st.text_input("Người cập nhật")
    f["G"]["updated_date"] = datetime.now().strftime("%d/%m/%Y")
    f["G"]["version"] = st.text_input("Phiên bản form","v1.0")
    f["G"]["note"] = st.text_area("Ghi chú")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 LƯU TẠM"):
            fn = f"DRAFT_{f['A']['A1'].get('system_code','NA')}.json"
            with open(os.path.join(DATA_DIR,fn),"w",encoding="utf-8") as fp:
                json.dump(f,fp,ensure_ascii=False,indent=2)
            st.success(f"Đã lưu tạm: {fn}")

    with col2:
        if st.button("✅ HOÀN TẤT"):
            fn = f"{f['A']['A1'].get('system_code','NA')}.json"
            with open(os.path.join(DATA_DIR,fn),"w",encoding="utf-8") as fp:
                json.dump(f,fp,ensure_ascii=False,indent=2)
            st.success(f"Đã lưu chính thức: {fn}")

    st.markdown("</div>", unsafe_allow_html=True)
