import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# ==============================================================================
# 1. CẤU HÌNH TRANG ĐẦU TIÊN (MUST BE FIRST)
# ==============================================================================
st.set_page_config(
    layout="wide",
    page_title="Hệ Thống Phát Hiện Gian Lận Giao Dịch",
    page_icon="🛡️"
)

# ==============================================================================
# 2. HÀM NẠP DỮ LIỆU VÀ CACHE
# ==============================================================================
@st.cache_data
def load_data(file_bytes, file_name):
    """Nạp dữ liệu từ bytes để đảm bảo khả năng hash của Streamlit cache."""
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_bytes)
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_bytes)
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file dữ liệu: {e}")
        return None

# Danh sách các đặc trưng (features) mặc định theo notebook
FEATURES = [f'X_{i}' for i in range(1, 15)]
TARGET = 'default'

# ==============================================================================
# 3. THÀNH PHẦN 1: SIDEBAR — VÙNG CẤU HÌNH
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Cấu hình & Tải dữ liệu")
    
    # Tải tệp dữ liệu huấn luyện
    uploaded_file = st.file_uploader(
        "Tải lên dữ liệu huấn luyện (.csv, .xlsx)", 
        type=["csv", "xlsx"],
        help="Tải lên tệp dữ liệu mẫu chứa các cột từ X_1 đến X_14 và cột mục tiêu 'default'."
    )
    
    st.divider()
    st.subheader("Tham số mô hình AI")
    st.caption("Thuật toán: Random Forest Classifier")
    
    # Các siêu tham số trích xuất và tối ưu từ notebook
    n_estimators = st.slider(
        "Số lượng cây (n_estimators)", 
        min_value=10, max_value=300, value=100, step=10,
        help="Số lượng cây quyết định trong rừng."
    )
    
    max_depth = st.slider(
        "Độ sâu tối đa (max_depth)", 
        min_value=2, max_value=30, value=15,
        help="Độ sâu tối đa của mỗi cây quyết định."
    )
    
    random_state = st.number_input(
        "Trạng thái ngẫu nhiên (random_state)", 
        value=42, step=1,
        help="Hạt giống ngẫu nhiên để đảm bảo tính tái lập của kết quả."
    )
    
    # Gom tham số nâng cao vào expander
    with st.expander("Tham số nâng cao"):
        criterion = st.selectbox(
            "Tiêu chí đánh giá (criterion)", 
            options=["gini", "entropy", "log_loss"], index=0,
            help="Hàm đo lường chất lượng phân tách phân lớp."
        )
        min_samples_split = st.slider(
            "Mẫu tối thiểu để tách nút (min_samples_split)", 
            min_value=2, max_value=10, value=2
        )

    st.divider()
    # Nút bấm kích hoạt huấn luyện duy nhất
    trigger_train = st.button(
        "🚀 Huấn luyện mô hình", 
        type="primary", 
        use_container_width=True,
        help="Bấm để bắt đầu quá trình trích xuất, phân tách và huấn luyện mô hình."
    )

# ==============================================================================
# 4. THÀNH PHẦN 2: HEADER — VÙNG ĐỊNH HƯỚNG
# ==============================================================================
st.title("🛡️ Hệ Thống Phát Hiện Giao Dịch Gian Lận")
st.caption("Ứng dụng hỗ trợ phân tích rủi ro tài chính và phát hiện sớm các hành vi gian lận giao dịch dựa trên học máy.")

# Kiểm tra trạng thái dữ liệu đầu vào
if uploaded_file is None:
    st.info("💡 Vui lòng tải tệp dữ liệu huấn luyện (.csv hoặc .xlsx) từ hộp công cụ Sidebar để bắt đầu.")
    st.stop()

# Đọc dữ liệu khi đã upload
df_main = load_data(uploaded_file, uploaded_file.name)
if df_main is None:
    st.error("Không thể xử lý dữ liệu. Vui lòng kiểm tra lại định dạng file.")
    st.stop()

st.caption(f"📁 Đang sử dụng tệp: **{uploaded_file.name}** | Số lượng bản ghi: {df_main.shape[0]} dòng, {df_main.shape[1]} cột.")
st.divider()

# ==============================================================================
# 5. KHỐI HUẤN LUYỆN (Xử lý khi bấm nút và lưu vào session_state)
# ==============================================================================
if trigger_train:
    with st.spinner("⏳ Đang huấn luyện mô hình Random Forest... Vui lòng đợi trong giây lát."):
        # Kiểm tra tính hợp lệ của các cột dữ liệu
        missing_cols = [col for col in FEATURES + [TARGET] if col not in df_main.columns]
        if missing_cols:
            st.error(f"Tệp dữ liệu thiếu các cột bắt buộc sau: {missing_cols}")
        else:
            # Chuẩn bị dữ liệu X, y
            X = df_main[FEATURES]
            y = df_main[TARGET]
            
            # Chia tập dữ liệu theo tỷ lệ chuẩn từ notebook
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
            
            # Khởi tạo và khớp mô hình
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                criterion=criterion,
                min_samples_split=min_samples_split,
                random_state=random_state
            )
            model.fit(X_train, y_train)
            
            # Dự đoán để tính toán chỉ số đánh giá
            y_pred = model.predict(X_test)
            
            # Lưu trữ vào session_state
            st.session_state['trained_model'] = model
            st.session_state['features_info'] = {
                'median': X_train.median().to_dict(),
                'min': X_train.min().to_dict(),
                'max': X_train.max().to_dict(),
                'list': FEATURES
            }
            st.session_state['metrics'] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'cm': confusion_matrix(y_test, y_pred),
                'report': classification_report(y_test, y_pred, output_dict=True)
            }
            st.success("🎉 Huấn luyện mô hình thành công! Hãy chuyển sang các tab bên dưới để xem kết quả và dự báo.")

# ==============================================================================
# 6. GIAO DIỆN CHÍNH PHÂN TAB
# ==============================================================================
tab_summary, tab_viz, tab_metrics, tab_inference = st.tabs([
    "📊 Tổng quan dữ liệu", 
    "📈 Trực quan hóa dữ liệu", 
    "🎯 Kết quả & Kiểm định", 
    "🔮 Sử dụng mô hình"
])

# ------------------------------------------------------------------------------
# TAB 1: TỔNG QUAN DỮ LIỆU
# ------------------------------------------------------------------------------
with tab_summary:
    st.subheader("Phân tích cấu trúc file dữ liệu")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Số lượng hàng (Rows)", f"{df_main.shape[0]:,}")
    col_m2.metric("Số lượng cột (Columns)", f"{df_main.shape[1]}")
    file_size_mb = uploaded_file.size / (1024 * 1024)
    col_m3.metric("Dung lượng tệp", f"{file_size_mb:.2f} MB")
    
    st.markdown("#### 📄 Xem trước dữ liệu thô (5 hàng đầu tiên)")
    st.dataframe(df_main.head(5), use_container_width=True)
    
    st.markdown("#### 📈 Thống kê mô tả các biến đặc trưng (Features)")
    available_features = [c for c in FEATURES if c in df_main.columns]
    if available_features:
        st.dataframe(df_main[available_features].describe().T, use_container_width=True)
    else:
        st.warning("Không tìm thấy các biến X_1 đến X_14 trong dữ liệu hiện tại.")

# ------------------------------------------------------------------------------
# TAB 2: TRỰC QUAN HÓA DỮ LIỆU
# ------------------------------------------------------------------------------
with tab_viz:
    st.subheader("Trực quan hóa phân phối biến")
    
    # Ưu tiên hiển thị biến mục tiêu trước
    if TARGET in df_main.columns:
        st.markdown("#### 🎯 Phân phối của biến mục tiêu Gian lận (`default`)")
        target_counts = df_main[TARGET].value_counts().reset_index()
        target_counts.columns = ['Trạng thái', 'Số lượng']
        target_counts['Trạng thái'] = target_counts['Trạng thái'].map({0: 'Hợp lệ (0)', 1: 'Gian lận (1)'})
        
        fig_target = px.bar(
            target_counts, x='Trạng thái', y='Số lượng', 
            color='Trạng thái', text_auto=True,
            title="Tỷ lệ phân lớp nhãn dữ liệu",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_target, use_container_width=True)
        st.divider()

    st.markdown("#### 📊 Phân phối các biến đặc trưng đầu vào số liên tục")
    selected_features = st.multiselect(
        "Chọn các biến đặc trưng để hiển thị biểu đồ phân phối (Mặc định chọn 4 biến đầu tiên):",
        options=FEATURES,
        default=FEATURES[:4]
    )
    
    if selected_features:
        # Tạo lưới biểu đồ 2x2 hoặc tùy biến theo số lượng chọn
        cols_viz = st.columns(2)
        for idx, feat in enumerate(selected_features):
            if feat in df_main.columns:
                with cols_viz[idx % 2]:
                    fig_feat = px.histogram(
                        df_main, x=feat, color=TARGET if TARGET in df_main.columns else None,
                        marginal="box", title=f"Biểu đồ phân phối biến {feat}",
                        barmode="overlay", color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_feat.update_layout(height=350)
                    st.plotly_chart(fig_feat, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: KẾT QUẢ HUẤN LUYỆN & KIỂM ĐỊNH MÔ HÌNH
# ------------------------------------------------------------------------------
with tab_metrics:
    st.subheader("Đánh giá hiệu năng mô hình")
    
    if 'trained_model' not in st.session_state:
        st.info("⚠️ Mô hình chưa được huấn luyện. Vui lòng thiết lập các tham số và nhấn nút 'Huấn luyện mô hình' ở thanh Sidebar bên trái.")
    else:
        metrics = st.session_state['metrics']
        
        # Thống kê dạng số vô hướng
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        col_t1.metric("Độ chính xác (Accuracy)", f"{metrics['accuracy']:.4f}")
        col_t2.metric("Độ chuẩn xác (Precision)", f"{metrics['precision']:.4f}")
        col_t3.metric("Độ nhạy (Recall)", f"{metrics['recall']:.4f}")
        col_t4.metric("Điểm F1-Score", f"{metrics['f1']:.4f}")
        
        st.divider()
        col_l, col_r = st.columns(2)
        
        with col_l:
            st.markdown("#### 🧮 Ma trận nhầm lẫn (Confusion Matrix)")
            cm = metrics['cm']
            # Trực quan hóa ma trận nhầm lẫn bằng plotly heatmap
            fig_cm = px.imshow(
                cm, text_auto=True,
                labels=dict(x="Nhãn Dự Đoán", y="Nhãn Thực Tế", color="Số lượng"),
                x=['Hợp lệ (0)', 'Gian lận (1)'],
                y=['Hợp lệ (0)', 'Gian lận (1)'],
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with col_r:
            st.markdown("#### 📋 Chi tiết báo cáo phân lớp (Classification Report)")
            report_df = pd.DataFrame(metrics['report']).transpose()
            st.dataframe(report_df.style.format(precision=4), use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: SỬ DỤNG MÔ HÌNH (DỰ BÁO)
# ------------------------------------------------------------------------------
with tab_inference:
    st.subheader("Chẩn đoán phân loại giao dịch gian lận")
    
    if 'trained_model' not in st.session_state:
        st.info("⚠️ Vui lòng cấu hình và nhấn nút 'Huấn luyện mô hình' ở thanh Sidebar trước khi sử dụng tính năng dự báo thực tế.")
    else:
        model = st.session_state['trained_model']
        feat_info = st.session_state['features_info']
        
        mode = st.radio(
            "Phương thức nạp dữ liệu dự báo:",
            options=["Chế độ 1: Nhập trực tiếp thông số", "Chế độ 2: Tải file dữ liệu hàng loạt"],
            horizontal=True
        )
        
        # ----------------------------------------------------------------------
        # CHẾ ĐỘ 1: NHẬP TRỰC TIẾP
        # ----------------------------------------------------------------------
        if mode == "Chế độ 1: Nhập trực tiếp thông số":
            st.markdown("#### Điền thông tin các chỉ số đặc trưng của giao dịch:")
            
            with st.form(key="single_inference_form"):
                # Tạo lưới để phân bổ 14 trường dữ liệu đầu vào gọn gàng
                input_data = {}
                grid_cols = st.columns(4)
                
                for idx, feat in enumerate(FEATURES):
                    col_idx = idx % 4
                    with grid_cols[col_idx]:
                        # Lấy giá trị mặc định dựa vào median từ tập dữ liệu huấn luyện
                        v_def = float(feat_info['median'].get(feat, 0.0))
                        v_min = float(feat_info['min'].get(feat, -100.0))
                        v_max = float(feat_info['max'].get(feat, 100.0))
                        
                        input_data[feat] = st.number_input(
                            label=f"Biến số {feat}",
                            min_value=None, max_value=None,
                            value=v_def,
                            format="%.6f",
                            help=f"Giá trị thực tế chạy từ {v_min:.2f} đến {v_max:.2f}"
                        )
                
                submit_predict = st.form_submit_button("🔮 Kiểm tra mức độ gian lận", type="primary", use_container_width=True)
                
                if submit_predict:
                    # Chuyển đổi dữ liệu input sang cấu trúc DataFrame chuẩn đặc trưng
                    df_input = pd.DataFrame([input_data])
                    
                    # Tiến hành dự đoán nhãn và xác suất
                    prediction = model.predict(df_input)[0]
                    probabilities = model.predict_proba(df_input)[0]
                    
                    st.divider()
                    if prediction == 1:
                        st.error(f"🚨 **CẢNH BÁO:** Giao dịch này có dấu hiệu **GIAN LẬN** (Nhãn: 1).")
                        st.metric(label="Xác suất rủi ro gian lận", value=f"{probabilities[1]*100:.2f}%")
                    else:
                        st.success(f"✅ **AN TOÀN:** Giao dịch được thẩm định **HỢP LỆ** (Nhãn: 0).")
                        st.metric(label="Xác suất an toàn", value=f"{probabilities[0]*100:.2f}%")

        # ----------------------------------------------------------------------
        # CHẾ ĐỘ 2: TẢI FILE HÀNG LOẠT
        # ----------------------------------------------------------------------
        else:
            st.markdown("#### Tải lên file chứa danh sách giao dịch mới cần chấm điểm rủi ro:")
            st.caption("Yêu cầu file định dạng xlsx hoặc csv và phải chứa đầy đủ 14 cột đặc trưng từ `X_1` đến `X_14`.")
            
            new_file = st.file_uploader("Chọn file dữ liệu mới cần dự báo:", type=["csv", "xlsx"], key="bulk_file")
            
            if new_file is not None:
                df_new = load_data(new_file, new_file.name)
                if df_new is not None:
                    # Kiểm tra schema đặc trưng đầu vào
                    missing_features = [f for f in FEATURES if f not in df_new.columns]
                    
                    if missing_features:
                        st.error(f"Lỗi cấu trúc tệp! Không thể xử lý dự báo do thiếu các cột biến sau: {missing_features}")
                    else:
                        # Thực hiện dự báo hàng loạt
                        X_new = df_new[FEATURES]
                        bulk_preds = model.predict(X_new)
                        bulk_probs = model.predict_proba(X_new)[:, 1] # Xác suất lớp rủi ro (1)
                        
                        # Gán kết quả vào dataframe
                        df_res = df_new.copy()
                        df_res['Dự báo (Kết quả)'] = bulk_preds
                        df_res['Xác suất Gian lận (%)'] = np.round(bulk_probs * 100, 2)
                        
                        st.markdown("#### 📝 Bảng kết quả tổng hợp dự đoán:")
                        st.dataframe(df_res, use_container_width=True)
                        
                        # Tạo file tải về dưới dạng CSV mã hóa utf-8-sig chống lỗi font tiếng Việt
                        csv_data = df_res.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 Tải xuống kết quả dự báo (.CSV)",
                            data=csv_data,
                            file_name="ket_qua_du_bao_gian_lan.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
