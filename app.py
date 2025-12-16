def ui_section_F():
    st.subheader("F. ĐÁNH GIÁ & ĐỊNH HƯỚNG QUY HOẠCH")

    st.slider("Mức độ phù hợp chiến lược số (1–5)", 1, 5, 3, key="F.phu_hop_chien_luoc_so")
    st.selectbox(
        "Mức độ sẵn sàng Cloud / AI",
        ["Chưa sẵn sàng", "Một phần", "Sẵn sàng", "Đã triển khai"],
        key="F.san_sang_cloud_ai",
    )
    st.selectbox(
        "Khả năng mở rộng (Scalability)",
        ["Thấp", "Trung bình", "Cao"],
        key="F.scalability",
    )

    st.markdown("### Đề xuất")
    st.radio(
        "Hướng xử lý",
        ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"],
        key="F.de_xuat",
        horizontal=True,
    )
    st.selectbox("Độ ưu tiên", ["High", "Medium", "Low"], key="F.do_uu_tien")
    st.text_area("Ghi chú/luận cứ đề xuất", key="F.ghi_chu_de_xuat")


def ui_section_G():
    st.subheader("G. THÔNG TIN QUẢN LÝ – LƯU TRỮ")

    st.text_input("Người cập nhật", key="G.nguoi_cap_nhat")
    st.text_input("Ngày cập nhật", key="G.ngay_cap_nhat", disabled=True)
    st.text_input("Phiên bản form", key="G.phien_ban_form", disabled=True)
    st.text_area("Ghi chú", key="G.ghi_chu")


# ----------------------------
# App Pages
# ----------------------------
def page_form():
    st.header("Nhập/Cập nhật khảo sát hệ thống CNTT")

    # Sidebar: load existing
    st.sidebar.subheader("Nạp dữ liệu có sẵn")
    df = load_all_responses()

    system_code_list = df["system_code"].dropna().unique().tolist() if not df.empty else []
    selected_code = st.sidebar.selectbox("Chọn Mã hệ thống để nạp", ["(Không nạp)"] + system_code_list)

    col_load1, col_load2 = st.sidebar.columns(2)
    if col_load1.button("Nạp", use_container_width=True):
        if selected_code != "(Không nạp)":
            payload = get_response_by_code(selected_code) or {}
            clear_form_keys()
            payload_to_session_state(payload)
            st.rerun()

    if col_load2.button("Xóa form", use_container_width=True):
        clear_form_keys()
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Thông tin cập nhật (meta)")
    meta_updated_by = st.sidebar.text_input("User cập nhật", key="meta.updated_by")
    allow_delete = st.sidebar.checkbox("Cho phép xóa bản ghi", value=False)

    # Set default quản trị G (nếu chưa có)
    if "G.nguoi_cap_nhat" not in st.session_state and meta_updated_by:
        st.session_state["G.nguoi_cap_nhat"] = meta_updated_by

    # Ensure default for disabled fields
    st.session_state["G.ngay_cap_nhat"] = datetime.now().isoformat(timespec="seconds")
    st.session_state["G.phien_ban_form"] = FORM_VERSION

    with st.form("survey_form", clear_on_submit=False):
        system_code, system_name, business_group = ui_section_A()
        ui_section_B()
        ui_section_C()
        ui_section_D()
        ui_section_E()
        ui_section_F()
        ui_section_G()

        submitted = st.form_submit_button("Lưu khảo sát", type="primary")

    # Handle submit
    if submitted:
        system_code = (system_code or "").strip()
        system_name = (system_name or "").strip()

        if not system_code:
            st.error("Vui lòng nhập **Mã hệ thống (System Code)**.")
            return

        updated_by = (meta_updated_by or "").strip() or (st.session_state.get("G.nguoi_cap_nhat") or "").strip()
        if not updated_by:
            st.error("Vui lòng nhập **User cập nhật** (sidebar) hoặc **Người cập nhật** (mục G).")
            return

        payload = get_form_payload()

        # Đồng bộ lại các trường quản trị
        payload.setdefault("G", {})
        payload["G"]["ngay_cap_nhat"] = datetime.now().isoformat(timespec="seconds")
        payload["G"]["phien_ban_form"] = FORM_VERSION
        payload["G"]["nguoi_cap_nhat"] = st.session_state.get("G.nguoi_cap_nhat", updated_by)

        upsert_response(
            system_code=system_code,
            system_name=system_name,
            business_group=business_group,
            updated_by=updated_by,
            payload=payload,
        )
        st.success(f"Đã lưu khảo sát cho hệ thống: {system_code} - {system_name}")

    # Optional: delete current loaded record
    st.sidebar.divider()
    st.sidebar.subheader("Xóa bản ghi")
    delete_code = st.sidebar.text_input("Nhập Mã hệ thống để xóa", key="meta.delete_code")
    if st.sidebar.button("Xóa", disabled=not allow_delete, use_container_width=True):
        dc = (delete_code or "").strip()
        if not dc:
            st.sidebar.error("Nhập Mã hệ thống cần xóa.")
        else:
            delete_by_code(dc)
            st.sidebar.success(f"Đã xóa: {dc}")
            clear_form_keys()
            st.rerun()


def page_list():
    st.header("Danh sách hệ thống đã khảo sát")

    df = load_all_responses()
    if df.empty:
        st.info("Chưa có dữ liệu.")
        return

    export_df = to_flat_export_df(df)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        bg = st.selectbox("Lọc theo nhóm nghiệp vụ", ["(Tất cả)"] + sorted(df["business_group"].dropna().unique().tolist()))
    with col2:
        status_col = "A3.tinh_trang"
        status_vals = sorted(export_df[status_col].dropna().unique().tolist()) if status_col in export_df.columns else []
        status = st.selectbox("Lọc theo tình trạng", ["(Tất cả)"] + status_vals)
    with col3:
        q = st.text_input("Tìm kiếm (code/name)", value="")

    view = export_df.copy()

    if bg != "(Tất cả)":
        view = view[view["meta.business_group"] == bg]

    if status != "(Tất cả)" and status_col in view.columns:
        view = view[view[status_col].fillna("") == status]

    if q.strip():
        qq = q.strip().lower()
        mask = (
            view["meta.system_code"].fillna("").str.lower().str.contains(qq)
            | view["meta.system_name"].fillna("").str.lower().str.contains(qq)
        )
        view = view[mask]

    show_cols = [
        "meta.system_code",
        "meta.system_name",
        "meta.business_group",
        "A3.tinh_trang",
        "A3.ke_hoach_3_5_nam",
        "B1.mo_hinh_ha_tang",
        "C1.pii",
        "F.de_xuat",
        "F.do_uu_tien",
        "meta.updated_by",
        "meta.updated_at",
    ]
    show_cols = [c for c in show_cols if c in view.columns]

    st.dataframe(view[show_cols], use_container_width=True, hide_index=True)


def page_dashboard():
    st.header("Dashboard tổng hợp")

    df = load_all_responses()
    if df.empty:
        st.info("Chưa có dữ liệu để tổng hợp.")
        return

    export_df = to_flat_export_df(df)

    total = len(export_df)
    pii_yes = 0
    if "C1.pii" in export_df.columns:
        pii_yes = (export_df["C1.pii"].fillna("").astype(str) == "Có").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số hệ thống", total)
    col2.metric("Hệ thống có PII", pii_yes)
    col3.metric("Tỷ lệ PII", f"{(pii_yes/total*100):.1f}%" if total else "0%")

    st.divider()

    def plot_bar(col_key: str, title: str):
        if col_key not in export_df.columns:
            st.caption(f"Không có cột: {col_key}")
            return
        s = export_df[col_key].fillna("N/A").astype(str)
        vc = s.value_counts().reset_index()
        vc.columns = [title, "count"]
        st.subheader(title)
        st.dataframe(vc, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        plot_bar("B1.mo_hinh_ha_tang", "Mô hình hạ tầng")
        plot_bar("A3.ke_hoach_3_5_nam", "Kế hoạch 3–5 năm")
    with c2:
        plot_bar("F.do_uu_tien", "Độ ưu tiên")
        plot_bar("F.de_xuat", "Đề xuất quy hoạch")


def page_export():
    st.header("Export dữ liệu")

    df = load_all_responses()
    if df.empty:
        st.info("Chưa có dữ liệu để export.")
        return

    st.write("Xuất Excel gồm:")
    st.markdown("- **RawData**: dữ liệu đã flatten theo key (A1…, B1…, …)\n- Các sheet Summary: thống kê nhanh theo một số trường")

    excel_bytes = build_export_excel(df)
    st.download_button(
        label="Tải Excel",
        data=excel_bytes,
        file_name=f"it_system_survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )

    st.divider()
    st.subheader("Xem nhanh dữ liệu flatten")
    export_df = to_flat_export_df(df)
    st.dataframe(export_df.head(50), use_container_width=True, hide_index=True)


# ----------------------------
# Main
# ----------------------------
def main():
    st.set_page_config(page_title="Khảo sát hệ thống CNTT", layout="wide")
    init_db()

    st.sidebar.title("Công cụ khảo sát hệ thống CNTT")
    page = st.sidebar.radio("Chức năng", ["Nhập/Cập nhật", "Danh sách", "Dashboard", "Export"], index=0)

    if page == "Nhập/Cập nhật":
        page_form()
    elif page == "Danh sách":
        page_list()
    elif page == "Dashboard":
        page_dashboard()
    else:
        page_export()


if __name__ == "__main__":
    main()
