import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import io

# 1) Cấu hình trang Streamlit đầu tiên
st.set_page_config(
    layout="wide",
    page_title="Hệ thống Phát hiện Giao dịch Gian lận",
    page_icon="🛡️"
)

# 2) Hàm nạp dữ liệu dùng chung có cache
@st.cache_data
def load_data(file_bytes, file_name):
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {e}")
        return None

# Các cột tính năng bắt buộc dựa trên notebook
FEATURE_COLS = [f"X_{i}" for i in range(1, 15)]
TARGET_COL = "default"

# 3) THÀNH PHẦN 1: SIDEBAR — VÙNG CẤU HÌNH
with st.sidebar:
    # Sử dụng khối màu để làm nổi bật tiêu đề phân vùng cấu hình
    st.info("### ⚙️ Cấu hình & Tải dữ liệu")
    
    # Tải dữ liệu
    uploaded_file = st.file_uploader(
        "Tải lên tệp dữ liệu (CSV hoặc Excel)", 
        type=["csv", "xlsx", "xls"],
        help="Tải lên tệp chứa các cột dữ liệu X_1 đến X_14 và cột mục tiêu 'default'"
    )
    
    st.markdown("---")
    st.subheader("Tham số mô hình AI")
    st.caption("Thuật toán: RandomForestClassifier")
    
    # Siêu tham số trích xuất và tối ưu từ bài toán
    n_estimators = st.slider(
        "Số lượng cây (n_estimators)", 
        min_value=10, max_value=200, value=100, step=10,
        help="Số lượng cây quyết định trong rừng."
    )
    max_depth = st.slider(
        "Độ sâu tối đa (max_depth)", 
        min_value=2, max_value=20, value=10, step=1,
        help="Độ sâu tối đa của mỗi cây quyết định."
    )
    random_state = st.number_input(
        "Trạng thái ngẫu nhiên (random_state)", 
        value=42, step=1,
        help="Đảm bảo tính tái lập của kết quả huấn luyện."
    )
    
    st.markdown("---")
    # Nút bấm hành động duy nhất để huấn luyện
    train_clicked = st.button(
        "🚀 Huấn luyện mô hình", 
        type="primary", 
        use_container_width=True,
        help="Bấm để bắt đầu huấn luyện mô hình Random Forest với tham số đã chọn."
    )

# 4) THÀNH PHẦN 2: HEADER — VÙNG ĐỊNH HƯỚNG
st.title("🛡️ Hệ thống Phát hiện Giao dịch Gian lận")
st.caption("Ứng dụng phân tích và dự báo rủi ro gian lận tài chính dựa trên mô hình học máy Random Forest.")

if uploaded_file is None:
    st.info("💡 Vui lòng tải lên tệp dữ liệu mẫu (.csv hoặc .xlsx) ở thanh công cụ bên trái để bắt đầu.")
    st.stop()

# Đọc dữ liệu khi đã upload
file_bytes = uploaded_file.getvalue()
df = load_data(file_bytes, uploaded_file.name)

if df is None or df.empty:
    st.error("Tệp dữ liệu trống hoặc không đúng định dạng. Vui lòng kiểm tra lại.")
    st.stop()

# Tô màu xanh nhẹ cho phần trạng thái tệp dữ liệu đã nạp thành công
st.success(f"📁 Đang dùng tệp: **{uploaded_file.name}** | Số dòng: {df.shape[0]} | Số cột: {df.shape[1]}")
st.divider()

# 5) KHỐI HUẤN LUYỆN (Chạy khi bấm nút và lưu vào session_state)
if train_clicked:
    # Kiểm tra tính hợp lệ của dữ liệu trước khi train
    missing_cols = [col for col in FEATURE_COLS + [TARGET_COL] if col not in df.columns]
    if missing_cols:
        st.error(f"Thiếu các cột bắt buộc trong file dữ liệu: {missing_cols}")
    else:
        with st.spinner("Mô hình đang được huấn luyện, vui lòng đợi trong giây lát..."):
            X = df[FEATURE_COLS]
            y = df[TARGET_COL]
            
            # Chia tập dữ liệu giống quy trình ML chuẩn
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state, stratify=y)
            
            # Khởi tạo và huấn luyện mô hình
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
            model.fit(X_train, y_train)
            
            # Dự đoán trên tập kiểm tra
            y_pred = model.predict(X_test)
            
            # Lưu trữ vào session_state
            st.session_state['trained_model'] = model
            st.session_state['features'] = FEATURE_COLS
            st.session_state['metrics'] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'y_test': y_test,
                'y_pred': y_pred
            }
            st.success("🎉 Huấn luyện mô hình thành công! Hãy chuyển sang các Tab bên dưới để xem kết quả.")

# 6) KHỞI TẠO TABS NỘI DUNG
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tổng quan dữ liệu", 
    "📈 Trực quan hóa dữ liệu", 
    "🎯 Kết quả huấn luyện", 
    "🔮 Sử dụng mô hình"
])

# ---------------------------------------------------------
# THÀNH PHẦN 3: TAB "TỔNG QUAN DỮ LIỆU"
# ---------------------------------------------------------
with tab1:
    st.subheader("Thống kê số lượng cấu trúc dữ liệu")
    col1, col2, col3 = st.columns(3)
    col1.metric("Số lượng dòng (Records)", f"{df.shape[0]:,}")
    col2.metric("Số lượng cột (Features)", f"{df.shape[1]}")
    file_size_mb = len(file_bytes) / (1024 * 1024)
    col3.metric("Dung lượng tệp", f"{file_size_mb:.2f} MB")
    
    st.subheader("Xem trước dữ liệu thô (5 dòng đầu)")
    st.dataframe(df.head(), use_container_width=True)
    
    st.subheader("Thống kê mô tả các biến đặc trưng (X_1 đến X_14)")
    available_features = [c for c in FEATURE_COLS if c in df.columns]
    if available_features:
        st.dataframe(df[available_features].describe().T, use_container_width=True)
    else:
        st.warning("Không tìm thấy các biến X_1 đến X_14 để mô tả.")

# ---------------------------------------------------------
# THÀNH PHẦN 4: TAB "TRỰC QUAN HÓA DỮ LIỆU"
# ---------------------------------------------------------
with tab2:
    st.subheader("Biểu đồ phân tích phân phối thuộc tính")
    
    # Đặt ưu tiên biến mục tiêu trước
    cols_to_plot = []
    if TARGET_COL in df.columns:
        cols_to_plot.append(TARGET_COL)
    
    # Thêm các cột tính năng có sẵn
    available_features = [c for c in FEATURE_COLS if c in df.columns]
    cols_to_plot.extend(available_features[:3]) # Lấy 3 biến đầu mặc định
    
    # Bộ chọn động nếu người dùng muốn xem biến khác
    all_selectable = [c for c in df.columns]
    selected_features = st.multiselect("Chọn các trường thông tin cần vẽ biểu đồ (Tối đa hiển thị 4):", all_selectable, default=cols_to_plot[:4])
    
    if selected_features:
        # Giới hạn tối đa hiển thị bố cục 4 biểu đồ lưới 2x2
        display_features = selected_features[:4]
        
        # Tạo lưới 2x2 bằng 2 hàng columns
        for i in range(0, len(display_features), 2):
            row_cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < len(display_features):
                    col_name = display_features[idx]
                    with row_cols[j]:
                        if col_name == TARGET_COL or df[col_name].nunique() <= 5:
                            # Biến phân loại / Biến mục tiêu nhị phân
                            fig = px.histogram(
                                df, x=col_name, color=col_name if col_name == TARGET_COL else None,
                                title=f"Phân phối tần suất lớp - Cột {col_name}",
                                barmode='group', height=300
                            )
                        else:
                            # Biến số liên tục
                            fig = px.histogram(
                                df, x=col_name, title=f"Phân phối mật độ - Cột {col_name}",
                                marginal="box", height=300
                            )
                        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Vui lòng chọn ít nhất một cột dữ liệu để trực quan hóa.")

# ---------------------------------------------------------
# THÀNH PHẦN 5: TAB "KẾT QUẢ HUẤN LUYỆN & KIỂM ĐỊNH MÔ HÌNH"
# ---------------------------------------------------------
with tab3:
    if 'trained_model' not in st.session_state:
        st.info("⚠️ Vui lòng tùy chỉnh tham số và nhấn nút [🚀 Huấn luyện mô hình] tại thanh Sidebar bên trái để xem kết quả kiểm định.")
    else:
        metrics = st.session_state['metrics']
        
        # Thêm thông báo màu sắc phân vùng kết quả huấn luyện
        st.success("### ✅ Kết quả đánh giá hiệu năng mô hình (Tập Test)")
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Độ chính xác (Accuracy)", f"{metrics['accuracy']:.4f}")
        m_col2.metric("Độ chuẩn xác (Precision)", f"{metrics['precision']:.4f}", help="Tỷ lệ giao dịch cảnh báo gian lận chính xác thực tế")
        m_col3.metric("Độ phủ (Recall)", f"{metrics['recall']:.4f}", help="Tỷ lệ phát hiện được trên tổng số ca gian lận thực tế")
        m_col4.metric("F1-Score", f"{metrics['f1']:.4f}")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Ma trận nhầm lẫn (Confusion Matrix)")
            cm = confusion_matrix(metrics['y_test'], metrics['y_pred'])
            cm_df = pd.DataFrame(cm, index=['Thực tế: Bình thường (0)', 'Thực tế: Gian lận (1)'], 
                                     columns=['Dự đoán: Bình thường (0)', 'Dự đoán: Gian lận (1)'])
            st.dataframe(cm_df, use_container_width=True)
            
        with c2:
            st.subheader("Báo cáo chi tiết (Classification Report)")
            report = classification_report(metrics['y_test'], metrics['y_pred'], output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df.style.format(precision=4), use_container_width=True)

        # Trực quan tầm quan trọng của các biến tính năng
        st.subheader("Mức độ quan trọng của các biến số đặc trưng (Feature Importance)")
        model = st.session_state['trained_model']
        importance = model.feature_importances_
        feat_imp_df = pd.DataFrame({
            'Tính năng': st.session_state['features'],
            'Mức độ đóng góp': importance
        }).sort_values(by='Mức độ đóng góp', ascending=True)
        
        fig_imp = px.bar(feat_imp_df, x='Mức độ đóng góp', y='Tính năng', orientation='h',
                         title="Biểu đồ xếp hạng đóng góp tính năng của mô hình Random Forest", height=400)
        st.plotly_chart(fig_imp, use_container_width=True)

# ---------------------------------------------------------
# THÀNH PHẦN 6: TAB "SỬ DỤNG MÔ HÌNH"
# ---------------------------------------------------------
with tab4:
    if 'trained_model' not in st.session_state:
        st.info("⚠️ Vui lòng huấn luyện mô hình thành công tại Sidebar trước khi thực hiện chức năng dự báo rủi ro.")
    else:
        model = st.session_state['trained_model']
        
        # Sử dụng thông báo khối màu xanh dương để định hướng chọn chế độ
        st.info("### 🔮 Phân tích & Dự báo giao dịch mới")
        
        mode = st.radio(
            "Chọn phương thức nhập dữ liệu đầu vào:",
            ["Cách 1: Nhập trực tiếp thông số", "Cách 2: Tải file dữ liệu kiểm tra hàng loạt"],
            horizontal=True
        )
        
        # Tạo dữ liệu thống kê mẫu dựa trên dataframe ban đầu để làm giá trị mặc định (median)
        default_inputs = {}
        for col in FEATURE_COLS:
            if col in df.columns:
                default_inputs[col] = float(df[col].median())
            else:
                default_inputs[col] = 0.0

        if mode == "Cách 1: Nhập trực tiếp thông số":
            st.write("👉 Vui lòng điền thông số các trường đặc trưng bên dưới để kiểm tra giao dịch lẻ:")
            
            with st.form("single_prediction_form"):
                # Gom các ô nhập liệu vào các cột cho gọn giao diện
                form_cols = st.columns(4)
                input_data = {}
                
                for idx, col_name in enumerate(FEATURE_COLS):
                    col_pos = idx % 4
                    with form_cols[col_pos]:
                        input_data[col_name] = st.number_input(
                            f"Giá trị {col_name}", 
                            value=default_inputs[col_name],
                            format="%.6f"
                        )
                
                submit_pred = st.form_submit_button("🛡️ Kiểm tra mức độ rủi ro", type="primary")
                
                if submit_pred:
                    # Tạo cấu trúc DataFrame đúng thứ tự các cột lúc train
                    input_df = pd.DataFrame([input_data])[FEATURE_COLS]
                    
                    # Tiến hành dự báo
                    prediction = model.predict(input_df)[0]
                    probabilities = model.predict_proba(input_df)[0]
                    
                    st.markdown("### Kết quả phân tích:")
                    if prediction == 1:
                        st.error(f"🚨 CẢNH BÁO: Giao dịch có dấu hiệu **GIAN LẬN** (Tỷ lệ chắc chắn: {probabilities[1]*100:.2f}%)")
                    else:
                        st.success(f"✅ AN TOÀN: Giao dịch được phân loại **BÌNH THƯỜNG** (Tỷ lệ chắc chắn: {probabilities[0]*100:.2f}%)")
                        
        elif mode == "Cách 2: Tải file dữ liệu kiểm tra hàng loạt":
            st.write("👉 Tải lên tệp tin định dạng CSV/Excel chứa đầy đủ 14 biến số đặc trưng (`X_1` đến `X_14`) để thực hiện chấm điểm tự động.")
            
            bulk_file = st.file_uploader("Tải tệp kiểm tra (X_new)", type=["csv", "xlsx", "xls"], key="bulk_uploader")
            
            if bulk_file is not None:
                bulk_bytes = bulk_file.getvalue()
                bulk_df = load_data(bulk_bytes, bulk_file.name)
                
                if bulk_df is not None:
                    # Kiểm tra sự tương thích của các cột tính năng đầu vào
                    missing_features = [col for col in FEATURE_COLS if col not in bulk_df.columns]
                    
                    if missing_features:
                        st.error(f"Tệp tải lên không hợp lệ. Thiếu các cột đặc trưng sau: {missing_features}")
                    else:
                        # Thực hiện dự báo hàng loạt
                        X_new = bulk_df[FEATURE_COLS]
                        bulk_preds = model.predict(X_new)
                        bulk_probs = model.predict_proba(X_new)[:, 1] # Xác suất thuộc lớp gian lận (1)
                        
                        # Gán kết quả vào DataFrame hiển thị
                        result_df = bulk_df.copy()
                        result_df['Dự đoán phân loại (Prediction)'] = bulk_preds
                        result_df['Xác suất gian lận (Fraud Probability)'] = bulk_probs
                        
                        st.subheader("Bảng kết quả chấm điểm hàng loạt")
                        st.dataframe(result_df, use_container_width=True)
                        
                        # Tạo nút tải file kết quả về máy
                        output = io.BytesIO()
                        result_df.to_csv(output, index=False, encoding='utf-8-sig')
                        processed_data = output.getvalue()
                        
                        st.download_button(
                            label="📥 Tải xuống tệp kết quả dự báo (.CSV)",
                            data=processed_data,
                            file_name="ket_qua_du_bao_gian_lan.csv",
                            mime="text/csv"
                        )
