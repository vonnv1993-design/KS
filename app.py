import streamlit as st
import pandas as pd
from datetime import datetime
import json
from io import BytesIO
from fpdf import FPDF

# Cấu hình trang
st.set_page_config(
    page_title="Khảo sát Hệ thống CNTT",
    page_icon="📋",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #2ca02c;
        border-bottom: 2px solid #2ca02c;
        padding-bottom: 10px;
    }
    .section-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'survey_data' not in st.session_state:
    st.session_state.survey_data = {}

# Header
st.title("📋 PHIẾU KHẢO SÁT HỆ THỐNG CÔNG NGHỆ THÔNG TIN")
st.markdown("---")

# Tabs chính
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Khảo sát", 
    "📊 Xem dữ liệu", 
    "💾 Xuất file",
    "📈 Thống kê"
])

# ==================== TAB 1: KHẢO SÁT ====================
with tab1:
    with st.form("survey_form"):
        
        # ========== A. THÔNG TIN CHUNG ==========
        st.header("A. THÔNG TIN CHUNG")
        
        with st.expander("A1. Thông tin định danh hệ thống", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                ten_he_thong = st.text_input("Tên hệ thống/phần mềm *", key="ten_he_thong")
                ma_he_thong = st.text_input("Mã hệ thống (System Code) *", key="ma_he_thong")
                
            with col2:
                business_owner = st.text_input("Đơn vị sở hữu nghiệp vụ (Business Owner)", key="business_owner")
                it_owner = st.text_input("Đơn vị quản lý CNTT (IT Owner)", key="it_owner")
            
            nha_cung_cap = st.text_input("Nhà cung cấp / Đối tác", key="nha_cung_cap")
            
            st.write("**Nhóm nghiệp vụ:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                nghiep_vu_1 = st.checkbox("Khai thác bay")
                nghiep_vu_2 = st.checkbox("Thương mại")
            with col2:
                nghiep_vu_3 = st.checkbox("Dịch vụ")
                nghiep_vu_4 = st.checkbox("Kỹ thuật")
            with col3:
                nghiep_vu_5 = st.checkbox("Tài chính")
                nghiep_vu_6 = st.checkbox("Nhân sự")
            with col4:
                nghiep_vu_7 = st.checkbox("An toàn – An ninh")
                nghiep_vu_8 = st.checkbox("Quản lý chung")
            
            st.write("**Loại hệ thống:**")
            loai_he_thong = st.multiselect(
                "Chọn loại hệ thống",
                ["COTS", "SaaS", "In-house", "Outsource", "Legacy"],
                key="loai_he_thong"
            )
            
            st.write("**Vai trò trong chuỗi giá trị hàng không:**")
            vai_tro = st.multiselect(
                "Chọn vai trò",
                ["Core", "Support", "Analytics", "Compliance"],
                key="vai_tro"
            )
        
        with st.expander("A2. Mục tiêu & phạm vi"):
            muc_tieu = st.text_area("Mục tiêu nghiệp vụ chính", key="muc_tieu")
            pham_vi = st.text_area("Phạm vi chức năng", key="pham_vi")
            doi_tuong = st.text_input("Đối tượng người dùng", key="doi_tuong")
            
            so_luong_user = st.radio(
                "Số lượng user (hiện tại / dự kiến 3–5 năm)",
                ["< 10 người", "10-50 người", "50-100 người", "> 100 người"],
                key="so_luong_user"
            )
            
            khu_vuc = st.multiselect(
                "Khu vực sử dụng",
                ["Nội địa", "Quốc tế", "Toàn mạng"],
                key="khu_vuc"
            )
        
        with st.expander("A3. Tình trạng & vòng đời"):
            col1, col2 = st.columns(2)
            
            with col1:
                nam_trien_khai = st.selectbox(
                    "Năm triển khai",
                    range(2000, 2051),
                    index=24,  # 2024
                    key="nam_trien_khai"
                )
                
                tinh_trang = st.radio(
                    "Tình trạng hiện tại",
                    ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"],
                    key="tinh_trang"
                )
            
            with col2:
                muc_do_dap_ung = st.slider(
                    "Đánh giá mức độ đáp ứng nghiệp vụ",
                    1, 5, 3,
                    key="muc_do_dap_ung"
                )
                
                ke_hoach = st.multiselect(
                    "Kế hoạch 3–5 năm",
                    ["Giữ nguyên", "Nâng cấp", "Thay thế", "Hợp nhất"],
                    key="ke_hoach"
                )
        
        # ========== B. THÔNG TIN VỀ HẠ TẦNG ==========
        st.header("B. THÔNG TIN VỀ HẠ TẦNG (INFRASTRUCTURE)")
        
        with st.expander("B1. Mô hình triển khai"):
            mo_hinh_ha_tang = st.multiselect(
                "Mô hình hạ tầng",
                ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"],
                key="mo_hinh_ha_tang"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                vi_tri_dc = st.text_input("Vị trí DC/Cloud Region", key="vi_tri_dc")
            with col2:
                nha_cung_cap_ha_tang = st.multiselect(
                    "Nhà cung cấp hạ tầng",
                    ["AWS", "Azure", "Viettel", "VNPT", "FPT", "Khác"],
                    key="nha_cung_cap_ha_tang"
                )
        
        with st.expander("B2. Tài nguyên hạ tầng"):
            col1, col2 = st.columns(2)
            
            with col1:
                may_chu = st.radio("Máy chủ", ["VM", "Physical"], key="may_chu")
                he_dieu_hanh = st.text_input("Hệ điều hành", key="he_dieu_hanh")
                cpu_ram_storage = st.text_input("CPU / RAM / Storage", key="cpu_ram_storage")
            
            with col2:
                database = st.text_input("Database Engine", key="database")
                middleware = st.text_input("Middleware", key="middleware")
                network = st.text_input("Network (LAN/WAN/MPLS/VPN)", key="network")
        
        with st.expander("B3. Tính sẵn sàng & an toàn"):
            col1, col2 = st.columns(2)
            
            with col1:
                sla = st.select_slider(
                    "SLA (% uptime)",
                    options=["90-95%", "95-99%", "99-99.9%", "99.9-100%"],
                    key="sla"
                )
                
                ha_dr = st.radio(
                    "HA/DR",
                    ["Active-Active", "Active-Passive", "None"],
                    key="ha_dr"
                )
            
            with col2:
                rpo_rto = st.text_input("RPO / RTO", key="rpo_rto")
                
                sao_luu = st.multiselect(
                    "Sao lưu dữ liệu",
                    ["Hàng ngày", "Thời gian thực"],
                    key="sao_luu"
                )
            
            tuan_thu = st.multiselect(
                "Tuân thủ tiêu chuẩn",
                ["ISO 27001", "PCI DSS", "ICAO", "IATA"],
                key="tuan_thu"
            )
        
        # ========== C. THÔNG TIN VỀ DỮ LIỆU ==========
        st.header("C. THÔNG TIN VỀ DỮ LIỆU (DATA)")
        
        with st.expander("C1. Loại dữ liệu"):
            col1, col2 = st.columns(2)
            
            with col1:
                du_lieu_ca_nhan = st.radio("Dữ liệu cá nhân (PII)", ["Có", "Không"], key="du_lieu_ca_nhan")
                du_lieu_nhay_cam = st.radio("Dữ liệu nhạy cảm / an ninh hàng không", ["Có", "Không"], key="du_lieu_nhay_cam")
            
            with col2:
                du_lieu_tai_chinh = st.radio("Dữ liệu tài chính / thanh toán", ["Có", "Không"], key="du_lieu_tai_chinh")
                du_lieu_roi_vn = st.radio("Dữ liệu có rời Việt Nam", ["Có", "Không"], key="du_lieu_roi_vn")
            
            du_lieu_nghiep_vu = st.text_area(
                "Dữ liệu nghiệp vụ chính và các dữ liệu nhạy cảm/trọng yếu",
                key="du_lieu_nghiep_vu"
            )
        
        with st.expander("C2. Quản lý & chất lượng dữ liệu"):
            col1, col2 = st.columns(2)
            
            with col1:
                nguon_du_lieu = st.text_input("Nguồn dữ liệu (Source of Truth)", key="nguon_du_lieu")
                
                dinh_dang = st.multiselect(
                    "Định dạng dữ liệu",
                    ["Structured", "Semi-structured", "Unstructured"],
                    key="dinh_dang"
                )
            
            with col2:
                dung_luong = st.text_input("Dung lượng dữ liệu (hiện tại / tăng trưởng năm)", key="dung_luong")
                chinh_sach = st.text_input("Chính sách lưu trữ & xóa dữ liệu", key="chinh_sach")
            
            chat_luong = st.multiselect(
                "Chất lượng dữ liệu",
                ["Đầy đủ", "Chính xác", "Kịp thời"],
                key="chat_luong"
            )
        
        with st.expander("C3. Khai thác & phân tích"):
            col1, col2 = st.columns(2)
            
            with col1:
                bi_ai = st.radio("Có cung cấp dữ liệu cho BI/AI không", ["Có", "Không"], key="bi_ai")
                data_warehouse = st.radio("Kết nối Data Warehouse / Data Lake", ["Có", "Không"], key="data_warehouse")
            
            with col2:
                tan_suat_dong_bo = st.text_input("Tần suất đồng bộ dữ liệu", key="tan_suat_dong_bo")
                real_time = st.radio("Dữ liệu thời gian thực (Real-time)", ["Có", "Không"], key="real_time")
        
                with col3:
                    sys_integration = st.multiselect(
                        f"Hình thức tích hợp",
                        ["API", "ESB", "Message Queue", "File", "Manual"],
                        key=f"sys_integration_{i}"
                    )
                with col4:
                    sys_note = st.text_input(f"Ghi chú", key=f"sys_note_{i}")
                
                integrated_systems.append({
                    "STT": i+1,
                    "Tên hệ thống": sys_name,
                    "Vai trò": ", ".join(sys_role),
                    "Hình thức tích hợp": ", ".join(sys_integration),
                    "Ghi chú": sys_note
                })
        
        with st.expander("D2. Chuẩn & giao thức"):
            col1, col2 = st.columns(2)
            
            with col1:
                chuan_du_lieu = st.multiselect(
                    "Chuẩn dữ liệu",
                    ["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON", "Khác"],
                    key="chuan_du_lieu"
                )
                
                if "Khác" in chuan_du_lieu:
                    chuan_khac = st.text_input("Nhập chuẩn khác", key="chuan_khac")
            
            with col2:
                giao_thuc = st.multiselect(
                    "Giao thức",
                    ["REST", "SOAP", "MQ", "SFTP"],
                    key="giao_thuc"
                )
                
                tan_suat_tich_hop = st.radio(
                    "Tần suất tích hợp",
                    ["Real-time", "Near real-time", "Batch"],
                    key="tan_suat_tich_hop"
                )
        
        with st.expander("D3. Quản trị tích hợp"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                api_gateway = st.radio("Có API Gateway không", ["Có", "Không"], key="api_gateway")
            with col2:
                logging = st.radio("Có logging / monitoring không", ["Có", "Không"], key="logging")
            with col3:
                version_api = st.radio("Quản lý version API", ["Có", "Không"], key="version_api")
        
        # ========== E. THÔNG TIN AN TOÀN – TUÂN THỦ ==========
        st.header("E. THÔNG TIN AN TOÀN – TUÂN THỦ")
        
        with st.expander("E. An toàn & Tuân thủ", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                phan_quyen = st.text_area("Phân quyền truy cập (RBAC)", key="phan_quyen")
                
                xac_thuc = st.multiselect(
                    "Xác thực",
                    ["SSO", "MFA", "Khác"],
                    key="xac_thuc"
                )
                
                if "Khác" in xac_thuc:
                    xac_thuc_khac = st.text_input("Nhập phương thức xác thực khác", key="xac_thuc_khac")
            
            with col2:
                ma_hoa = st.multiselect(
                    "Mã hóa dữ liệu",
                    ["At-rest", "In-transit"],
                    key="ma_hoa"
                )
                
                tuan_thu_phap_ly = st.multiselect(
                    "Tuân thủ pháp lý",
                    ["GDPR", "Luật ATTT VN", "ICAO Annex 17", "Quy chế ANTT TCTHK"],
                    key="tuan_thu_phap_ly"
                )
        
        # ========== F. ĐÁNH GIÁ & ĐỊNH HƯỚNG QUY HOẠCH ==========
        st.header("F. ĐÁNH GIÁ & ĐỊNH HƯỚNG QUY HOẠCH")
        
        with st.expander("F. Đánh giá & Định hướng", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                muc_do_phu_hop = st.slider(
                    "Mức độ phù hợp chiến lược số (1–5)",
                    1, 5, 3,
                    key="muc_do_phu_hop"
                )
                
                san_sang_cloud = st.text_area("Mức độ sẵn sàng Cloud / AI", key="san_sang_cloud")
                
                kha_nang_mo_rong = st.text_area("Khả năng mở rộng (Scalability)", key="kha_nang_mo_rong")
            
            with col2:
                de_xuat = st.multiselect(
                    "Đề xuất",
                    ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"],
                    key="de_xuat"
                )
                
                do_uu_tien = st.radio(
                    "Độ ưu tiên",
                    ["High", "Medium", "Low"],
                    key="do_uu_tien"
                )
        
        # ========== G. THÔNG TIN QUẢN LÝ – LƯU TRỮ ==========
        st.header("G. THÔNG TIN QUẢN LÝ – LƯU TRỮ")
        
        with st.expander("G. Thông tin quản lý", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nguoi_cap_nhat = st.text_input("Người cập nhật *", key="nguoi_cap_nhat")
                ngay_cap_nhat = st.date_input("Ngày cập nhật", datetime.now(), key="ngay_cap_nhat")
            
            with col2:
                phien_ban = st.text_input("Phiên bản form", value="v1.0", key="phien_ban")
                ghi_chu = st.text_area("Ghi chú", key="ghi_chu")
        
        # Nút submit
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button("✅ Lưu khảo sát", use_container_width=True)
        
        if submitted:
            # Kiểm tra các trường bắt buộc
            if not ten_he_thong or not ma_he_thong or not nguoi_cap_nhat:
                st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
            else:
                # Thu thập tất cả dữ liệu
                survey_data = {
                    # A. THÔNG TIN CHUNG
                    "Tên hệ thống": ten_he_thong,
                    "Mã hệ thống": ma_he_thong,
                    "Nhóm nghiệp vụ": [
                        "Khai thác bay" if nghiep_vu_1 else "",
                        "Thương mại" if nghiep_vu_2 else "",
                        "Dịch vụ" if nghiep_vu_3 else "",
                        "Kỹ thuật" if nghiep_vu_4 else "",
                        "Tài chính" if nghiep_vu_5 else "",
                        "Nhân sự" if nghiep_vu_6 else "",
                        "An toàn – An ninh" if nghiep_vu_7 else "",
                        "Quản lý chung" if nghiep_vu_8 else ""
                    ],
                    "Business Owner": business_owner,
                    "IT Owner": it_owner,
                    "Nhà cung cấp": nha_cung_cap,
                    "Loại hệ thống": ", ".join(loai_he_thong),
                    "Vai trò": ", ".join(vai_tro),
                    "Mục tiêu nghiệp vụ": muc_tieu,
                    "Phạm vi chức năng": pham_vi,
                    "Đối tượng người dùng": doi_tuong,
                    "Số lượng user": so_luong_user,
                    "Khu vực sử dụng": ", ".join(khu_vuc),
                    "Năm triển khai": nam_trien_khai,
                    "Tình trạng": tinh_trang,
                    "Mức độ đáp ứng": muc_do_dap_ung,
                    "Kế hoạch 3-5 năm": ", ".join(ke_hoach),
                    
                    # B. HẠ TẦNG
                    "Mô hình hạ tầng": ", ".join(mo_hinh_ha_tang),
                    "Vị trí DC": vi_tri_dc,
                    "Nhà cung cấp hạ tầng": ", ".join(nha_cung_cap_ha_tang),
                    "Máy chủ": may_chu,
                    "Hệ điều hành": he_dieu_hanh,
                    "CPU/RAM/Storage": cpu_ram_storage,
                    "Database": database,
                    "Middleware": middleware,
                    "Network": network,
                    "SLA": sla,
                    "HA/DR": ha_dr,
                    "RPO/RTO": rpo_rto,
                    "Sao lưu": ", ".join(sao_luu),
                    "Tuân thủ tiêu chuẩn": ", ".join(tuan_thu),
                    
                    # C. DỮ LIỆU
                    "Dữ liệu cá nhân": du_lieu_ca_nhan,
                    "Dữ liệu nhạy cảm": du_lieu_nhay_cam,
                    "Dữ liệu tài chính": du_lieu_tai_chinh,
                    "Dữ liệu rời VN": du_lieu_roi_vn,
                    "Dữ liệu nghiệp vụ": du_lieu_nghiep_vu,
                    "Nguồn dữ liệu": nguon_du_lieu,
                    "Định dạng dữ liệu": ", ".join(dinh_dang),
                    "Dung lượng": dung_luong,
                    "Chính sách lưu trữ": chinh_sach,
                    "Chất lượng dữ liệu": ", ".join(chat_luong),
                    "BI/AI": bi_ai,
                    "Data Warehouse": data_warehouse,
                    "Tần suất đồng bộ": tan_suat_dong_bo,
                    "Real-time": real_time,
                    
                    # D. TÍCH HỢP
                    "Hệ thống tích hợp": integrated_systems,
                    "Chuẩn dữ liệu": ", ".join(chuan_du_lieu),
                    "Giao thức": ", ".join(giao_thuc),
                    "Tần suất tích hợp": tan_suat_tich_hop,
                    "API Gateway": api_gateway,
                    "Logging/Monitoring": logging,
                    "Version API": version_api,
                    
                    # E. AN TOÀN
                    "Phân quyền": phan_quyen,
                    "Xác thực": ", ".join(xac_thuc),
                    "Mã hóa": ", ".join(ma_hoa),
                    "Tuân thủ pháp lý": ", ".join(tuan_thu_phap_ly),
                    
                    # F. ĐÁNH GIÁ
                    "Phù hợp chiến lược số": muc_do_phu_hop,
                    "Sẵn sàng Cloud/AI": san_sang_cloud,
                    "Khả năng mở rộng": kha_nang_mo_rong,
                    "Đề xuất": ", ".join(de_xuat),
                    "Độ ưu tiên": do_uu_tien,
                    
                    # G. QUẢN LÝ
                    "Người cập nhật": nguoi_cap_nhat,
                    "Ngày cập nhật": ngay_cap_nhat.strftime("%d/%m/%Y"),
                    "Phiên bản": phien_ban,
                    "Ghi chú": ghi_chu,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Lưu vào session state
                if 'all_surveys' not in st.session_state:
                    st.session_state.all_surveys = []
                
                st.session_state.all_surveys.append(survey_data)
                st.session_state.survey_data = survey_data
                
                st.success("✅ Đã lưu khảo sát thành công!")
                st.balloons()

# ==================== TAB 2: XEM DỮ LIỆU ====================
with tab2:
    st.header("📊 Dữ liệu đã thu thập")
    
    if 'all_surveys' in st.session_state and len(st.session_state.all_surveys) > 0:
        # Hiển thị số lượng khảo sát
        st.info(f"📋 Tổng số khảo sát: **{len(st.session_state.all_surveys)}**")
        
        # Chọn khảo sát để xem
        survey_names = [f"{i+1}. {s['Tên hệ thống']} ({s['Mã hệ thống']})" 
                       for i, s in enumerate(st.session_state.all_surveys)]
        
        selected_survey = st.selectbox("Chọn khảo sát để xem chi tiết", survey_names)
        
        if selected_survey:
            idx = int(selected_survey.split(".")[0]) - 1
            data = st.session_state.all_surveys[idx]
            
            # Hiển thị dữ liệu theo sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏢 Thông tin chung")
                st.write(f"**Tên hệ thống:** {data['Tên hệ thống']}")
                                st.write(f"**Mã hệ thống:** {data['Mã hệ thống']}")
                st.write(f"**Business Owner:** {data['Business Owner']}")
                st.write(f"**IT Owner:** {data['IT Owner']}")
                st.write(f"**Loại hệ thống:** {data['Loại hệ thống']}")
                st.write(f"**Năm triển khai:** {data['Năm triển khai']}")
                st.write(f"**Tình trạng:** {data['Tình trạng']}")
            
            with col2:
                st.subheader("💻 Hạ tầng")
                st.write(f"**Mô hình:** {data['Mô hình hạ tầng']}")
                st.write(f"**Nhà cung cấp:** {data['Nhà cung cấp hạ tầng']}")
                st.write(f"**Database:** {data['Database']}")
                st.write(f"**SLA:** {data['SLA']}")
                st.write(f"**HA/DR:** {data['HA/DR']}")
            
            st.markdown("---")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("📁 Dữ liệu")
                st.write(f"**Dữ liệu cá nhân:** {data['Dữ liệu cá nhân']}")
                st.write(f"**Dữ liệu nhạy cảm:** {data['Dữ liệu nhạy cảm']}")
                st.write(f"**Định dạng:** {data['Định dạng dữ liệu']}")
                st.write(f"**BI/AI:** {data['BI/AI']}")
            
            with col4:
                st.subheader("🔗 Tích hợp")
                st.write(f"**Chuẩn dữ liệu:** {data['Chuẩn dữ liệu']}")
                st.write(f"**Giao thức:** {data['Giao thức']}")
                st.write(f"**API Gateway:** {data['API Gateway']}")
                st.write(f"**Tần suất:** {data['Tần suất tích hợp']}")
            
            st.markdown("---")
            
            # Hiển thị hệ thống tích hợp
            if data['Hệ thống tích hợp']:
                st.subheader("🔄 Các hệ thống tích hợp")
                df_systems = pd.DataFrame(data['Hệ thống tích hợp'])
                st.dataframe(df_systems, use_container_width=True)
            
            st.markdown("---")
            
            col5, col6 = st.columns(2)
            
            with col5:
                st.subheader("🔒 An toàn & Tuân thủ")
                st.write(f"**Xác thực:** {data['Xác thực']}")
                st.write(f"**Mã hóa:** {data['Mã hóa']}")
                st.write(f"**Tuân thủ pháp lý:** {data['Tuân thủ pháp lý']}")
            
            with col6:
                st.subheader("📈 Đánh giá")
                st.write(f"**Phù hợp chiến lược số:** {data['Phù hợp chiến lược số']}/5")
                st.write(f"**Đề xuất:** {data['Đề xuất']}")
                st.write(f"**Độ ưu tiên:** {data['Độ ưu tiên']}")
            
            st.markdown("---")
            st.info(f"👤 Cập nhật bởi: **{data['Người cập nhật']}** | 📅 Ngày: **{data['Ngày cập nhật']}**")
        
        # Hiển thị bảng tổng hợp
        st.markdown("---")
        st.subheader("📋 Bảng tổng hợp tất cả khảo sát")
        
        # Tạo DataFrame tổng hợp
        summary_data = []
        for survey in st.session_state.all_surveys:
            summary_data.append({
                "Tên hệ thống": survey['Tên hệ thống'],
                "Mã hệ thống": survey['Mã hệ thống'],
                "Loại": survey['Loại hệ thống'],
                "Tình trạng": survey['Tình trạng'],
                "Mô hình": survey['Mô hình hạ tầng'],
                "Đánh giá": f"{survey['Mức độ đáp ứng']}/5",
                "Ưu tiên": survey['Độ ưu tiên'],
                "Ngày cập nhật": survey['Ngày cập nhật']
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)
        
    else:
        st.warning("⚠️ Chưa có dữ liệu khảo sát nào. Vui lòng điền form ở tab 'Khảo sát'.")

# ==================== TAB 3: XUẤT FILE ====================
with tab3:
    st.header("💾 Xuất dữ liệu")
    
    if 'all_surveys' in st.session_state and len(st.session_state.all_surveys) > 0:
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Xuất Excel")
            st.write("Phù hợp cho phân tích và tổng hợp dữ liệu")
            
            # Tạo file Excel
            def create_excel():
                output = BytesIO()
                
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Sheet 1: Tổng hợp
                    summary_data = []
                    for survey in st.session_state.all_surveys:
                        summary_data.append({
                            "Tên hệ thống": survey['Tên hệ thống'],
                            "Mã hệ thống": survey['Mã hệ thống'],
                            "Business Owner": survey['Business Owner'],
                            "IT Owner": survey['IT Owner'],
                            "Loại hệ thống": survey['Loại hệ thống'],
                            "Vai trò": survey['Vai trò'],
                            "Năm triển khai": survey['Năm triển khai'],
                            "Tình trạng": survey['Tình trạng'],
                            "Mức độ đáp ứng": survey['Mức độ đáp ứng'],
                            "Mô hình hạ tầng": survey['Mô hình hạ tầng'],
                            "Database": survey['Database'],
                            "SLA": survey['SLA'],
                            "Độ ưu tiên": survey['Độ ưu tiên'],
                            "Người cập nhật": survey['Người cập nhật'],
                            "Ngày cập nhật": survey['Ngày cập nhật']
                        })
                    
                    df_summary = pd.DataFrame(summary_data)
                    df_summary.to_excel(writer, sheet_name='Tổng hợp', index=False)
                    
                    # Sheet 2: Chi tiết từng hệ thống
                    for idx, survey in enumerate(st.session_state.all_surveys):
                        # Tạo DataFrame cho từng khảo sát
                        detail_data = []
                        for key, value in survey.items():
                            if key != 'Hệ thống tích hợp':
                                detail_data.append({
                                    "Trường thông tin": key,
                                    "Giá trị": str(value)
                                })
                        
                        df_detail = pd.DataFrame(detail_data)
                        sheet_name = f"{survey['Mã hệ thống'][:20]}"  # Giới hạn 20 ký tự
                        df_detail.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        # Nếu có hệ thống tích hợp, thêm vào sheet riêng
                        if survey['Hệ thống tích hợp']:
                            df_integration = pd.DataFrame(survey['Hệ thống tích hợp'])
                            integration_sheet = f"{survey['Mã hệ thống'][:15]}_TH"
                            df_integration.to_excel(writer, sheet_name=integration_sheet, index=False)
                
                output.seek(0)
                return output
            
            excel_file = create_excel()
            
            st.download_button(
                label="📥 Tải xuống Excel",
                data=excel_file,
                file_name=f"Khao_sat_CNTT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.info("""
            **File Excel bao gồm:**
            - Sheet tổng hợp tất cả hệ thống
            - Sheet chi tiết từng hệ thống
            - Sheet tích hợp (nếu có)
            """)
        
        with col2:
            st.subheader("📄 Xuất PDF")
            st.write("Phù hợp cho lưu trữ và trình bày")
            
            # Tạo file PDF
            def create_pdf():
                pdf = FPDF()
                pdf.add_page()
                
                # Thêm font hỗ trợ Unicode (cần file font)
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "KHAO SAT HE THONG CNTT", ln=True, align="C")
                pdf.ln(10)
                
                for idx, survey in enumerate(st.session_state.all_surveys):
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(0, 10, f"{idx+1}. {survey['Mã hệ thống']}", ln=True)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 8, f"Ten he thong: {survey['Tên hệ thống']}", ln=True)
                    pdf.cell(0, 8, f"Tinh trang: {survey['Tình trạng']}", ln=True)
                    pdf.cell(0, 8, f"Mo hinh: {survey['Mô hình hạ tầng']}", ln=True)
                    pdf.cell(0, 8, f"Do uu tien: {survey['Độ ưu tiên']}", ln=True)
                    pdf.ln(5)
                
                return pdf.output(dest='S').encode('latin-1')
            
            pdf_file = create_pdf()
            
            st.download_button(
                label="📥 Tải xuống PDF",
                data=pdf_file,
                file_name=f"Khao_sat_CNTT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            st.info("""
            **File PDF bao gồm:**
            - Thông tin tổng hợp
            - Danh sách hệ thống
            - Thông tin cơ bản
            """)
        
        st.markdown("---")
        
        # Xuất JSON
        st.subheader("📦 Xuất JSON (Backup đầy đủ)")
        
        json_data = json.dumps(st.session_state.all_surveys, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="📥 Tải xuống JSON",
            data=json_data,
            file_name=f"Khao_sat_CNTT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.info("File JSON chứa toàn bộ dữ liệu chi tiết, có thể import lại vào hệ thống.")
        
    else:
        st.warning("⚠️ Chưa có dữ liệu để xuất. Vui lòng điền form khảo sát trước.")

# ==================== TAB 4: THỐNG KÊ ====================
with tab4:
    st.header("📈 Thống kê & Phân tích")
    
    if 'all_surveys' in st.session_state and len(st.session_state.all_surveys) > 0:
        
        # Metrics tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tổng số hệ thống", len(st.session_state.all_surveys))
        
        with col2:
            dang_van_hanh = sum(1 for s in st.session_state.all_surveys if s['Tình trạng'] == 'Đang vận hành')
            st.metric("Đang vận hành", dang_van_hanh)
        
        with col3:
            high_priority = sum(1 for s in st.session_state.all_surveys if s['Độ ưu tiên'] == 'High')
            st.metric("Ưu tiên cao", high_priority)
        
        with col4:
            avg_rating = sum(s['Mức độ đáp ứng'] for s in st.session_state.all_surveys) / len(st.session_state.all_surveys)
            st.metric("Đánh giá TB", f"{avg_rating:.1f}/5")
        
        st.markdown("---")
        
        # Biểu đồ
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Phân bố theo tình trạng")
            tinh_trang_count = {}
            for survey in st.session_state.all_surveys:
                status = survey['Tình trạng']
                tinh_trang_count[status] = tinh_trang_count.get(status, 0) + 1
            
            df_status = pd.DataFrame(list(tinh_trang_count.items()), columns=['Tình trạng', 'Số lượng'])
            st.bar_chart(df_status.set_index('Tình trạng'))
        
        with col2:
            st.subheader("📊 Phân bố theo độ ưu tiên")
            uu_tien_count = {}
                
