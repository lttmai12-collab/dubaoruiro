
Conversation with Gemini
dùng tiếng việt

Dạ sẵn sàng! Chúng ta sẽ trò chuyện bằng tiếng Việt nhé.

Tôi có thể giúp gì cho bạn hôm nay?

# PROMPT CHUẨN: CHUYỂN NOTEBOOK ML THÀNH WEB APP STREAMLIT

 

> Cách dùng: Tải lên **01 notebook (.ipynb)** + **01 file

dữ liệu mẫu**, rồi dán toàn bộ

> prompt này vào. AI sẽ sinh ra đúng 3 file: `app.py`,

`requirements.txt`, `README.md`.

 

---

 

## KHỐI MASTER — VAI TRÒ, QUY TRÌNH & QUY TẮC CHUNG

 

### VAI TRÒ

Bạn là kỹ sư Streamlit + Machine Learning giàu kinh nghiệm,

chuyên chuyển notebook

huấn luyện mô hình thành ứng dụng web Streamlit chuẩn, gọn,

chạy được ngay. Bạn thiết

kế giao diện theo nguyên tắc phân vùng (zoning) và best

practice layout của Streamlit:

cấu hình bền vững → sidebar; nội dung & kết quả → vùng

chính chia tab.

 

### ĐẦU VÀO

Người dùng đính kèm:

- 01 notebook (.ipynb) chứa quy trình: nạp dữ liệu, tiền xử

lý, huấn luyện và (có thể) kiểm định mô hình.

- 01 file dữ liệu (.csv/.xlsx...) là dữ liệu mẫu của ứng dụng.

 

### QUY TRÌNH BẮT BUỘC (làm theo thứ tự, KHÔNG bỏ bước)

1. ĐỌC KỸ NOTEBOOK và trích xuất CHÍNH XÁC:

   - Họ thuật toán

& tên mô hình (có thể có nhiều mô hình).

   - Tập biến đầu vào

X (tên cột, kiểu); biến mục tiêu y nếu có (giám sát) hoặc không có (không giám

sát).

   - Các bước tiền xử

lý (scaler, encoder, xử lý thiếu, tạo biến phái sinh...).

   - Siêu tham số và

GIÁ TRỊ người dùng đã đặt trong notebook (dùng làm mặc định trên giao diện).

   - Các chỉ tiêu kiểm

định notebook đã tính (để tái hiện đúng).

2. ĐỌC FILE DỮ LIỆU để biết: định dạng, danh sách cột, kiểu

dữ liệu, kích thước.

3. SINH ỨNG DỤNG theo đặc tả 6 thành phần bên dưới, ghép vào

MỘT file `app.py`.

4. TUYỆT ĐỐI không bịa biến/tham số/nghiệp vụ — mọi thứ phải

suy ra từ notebook + dữ liệu.

   Nếu notebook thiếu

thông tin, chọn mặc định hợp lý và GHI CHÚ trong README.

 

### QUY TẮC KỸ THUẬT CHUNG (áp dụng toàn app)

- `st.set_page_config(layout="wide",

page_title=..., page_icon=...)` là LỆNH STREAMLIT

  ĐẦU TIÊN của

`app.py` (trước cả sidebar).

- TÁI HIỆN ĐÚNG pipeline của notebook: cùng tập biến, cùng

tiền xử lý, cùng siêu tham số mặc định.

- Một HÀM nạp dữ liệu DÙNG CHUNG có `@st.cache_data`, nhận

bytes của file (để hashable),

  trả về DataFrame đã

tạo biến phái sinh giống notebook. Mọi nơi nạp dữ liệu đều gọi hàm này.

- HUẤN LUYỆN CHỈ MỘT LẦN khi người dùng bấm nút ở sidebar.

Lưu vào `st.session_state`

  BA thứ để mọi tab

dùng lại mà KHÔNG train lại khi chuyển tab:

    (1) mô hình đã

`fit`, (2) bộ tiền xử lý (scaler/encoder), (3) bảng kết quả đã chấm điểm.

- Mọi tab phụ thuộc kết quả phải kiểm tra `session_state`; nếu

chưa train thì hướng dẫn

  người dùng bấm nút

và dừng tab (không gây lỗi).

- Nhãn giao diện dùng tiếng Việt (hoặc theo ngôn ngữ của

notebook). Mỗi widget cấu hình có `help=` tooltip.

- Xử lý lỗi: file sai định dạng, thiếu cột, dữ liệu rỗng →

thông báo rõ ràng, không crash.

- KHÔNG dùng localStorage hay lưu trữ trình duyệt (không áp

dụng cho Streamlit).

 

### THỨ TỰ GHÉP CÁC THÀNH PHẦN TRONG `app.py`

1) `set_page_config` → 2) import & các hàm cache dùng

chung → 3) SIDEBAR (TP1)

→ 4) HEADER + kiểm tra dữ liệu (TP2) → 5) Khối train (chạy

khi bấm nút, lưu `session_state`)

→ 6) `st.tabs([...])` chứa TP3, TP4, TP5, TP6.

 

### ĐẦU RA — CHỈ TẠO ĐÚNG 3 FILE, KHÔNG THÊM

1. **app.py** — toàn bộ ứng dụng đã ghép từ 6 thành phần.

2. **requirements.txt** — liệt kê thư viện cần (suy từ

import trong notebook + thư viện app:

   streamlit, pandas,

plotly, scikit-learn, openpyxl nếu đọc/ghi Excel...). Ghi tên gói, có thể kèm

phiên bản tối thiểu.

3. **README.md** — gồm: mô tả app & mô hình dùng; cài đặt

(`pip install -r requirements.txt`);

   chạy (`streamlit

run app.py`); cấu trúc file dữ liệu đầu vào; mô tả ngắn từng tab; ghi chú

   phiên bản Streamlit

(khuyến nghị bản mới cho `st.container(horizontal=True)`, `st.space`, dynamic

container).

 

---

 

## THÀNH PHẦN 1: SIDEBAR — VÙNG CẤU HÌNH

 

Sidebar (`st.sidebar`) chứa MỌI điều khiển cấu hình bền vững.

KHÔNG đặt kết quả, biểu đồ, bảng ở đây.

 

Nội dung & thứ tự (theo luồng thao tác, trên → dưới):

1. TIÊU ĐỀ MỤC: `st.header`, ví dụ "⚙️

Cấu hình & Tải dữ liệu".

2. TẢI DỮ LIỆU: `st.file_uploader` đúng định dạng file dữ liệu

đính kèm.

3. LỰA CHỌN MÔ HÌNH — CHỈ thêm NẾU notebook dùng/đề cập nhiều

hơn một thuật toán

   (`st.selectbox`). Một

mô hình duy nhất thì bỏ qua mục này.

4. THAM SỐ MÔ HÌNH: `st.subheader` "Tham số mô hình

AI", bên dưới là widget tham số.

   Trích từ notebook:

tên siêu tham số, giá trị mặc định, kiểu widget phù hợp

   (slider cho số khoảng;

number_input cho số nguyên rời rạc như random_state;

   selectbox cho lựa

chọn rời rạc như kernel/criterion; checkbox cho cờ), khoảng giá trị hợp lý.

   Nhiều mô hình → hiển

thị tham số ĐỘNG theo mô hình đang chọn (if/elif), chỉ hiện

   tham số liên quan. Gom tham số nâng cao vào

`st.expander`.

5. NÚT HÀNH ĐỘNG: `st.button(..., type="primary",

use_container_width=True)` ở DƯỚI CÙNG,

   sau `st.divider()`.

Nhãn phản ánh đúng tác vụ. Đây là điểm DUY NHẤT kích hoạt huấn luyện.

 

Quy tắc: bao trong `with st.sidebar:`; sidebar CHỈ thu thập

cấu hình và trả về biến

(file, model_name, tham số, cờ "chạy") — KHÔNG huấn

luyện trong sidebar. Cân nhắc `st.form`

nếu muốn tránh rerun mỗi lần kéo slider.

 

---

 

## THÀNH PHẦN 2: HEADER — VÙNG ĐỊNH HƯỚNG

 

Nằm ở ĐẦU vùng chính (sau set_page_config & sidebar).

Giúp người dùng hiểu app là gì,

cần làm gì, dữ liệu đã sẵn sàng chưa.

 

Nội dung & thứ tự:

1. TIÊU ĐỀ: `st.title` + icon, nội dung SUY TỪ chủ đề

notebook (đọc markdown/mục tiêu), KHÔNG hardcode.

2. MÔ TẢ NGẮN: `st.caption` nêu app làm gì & đầu vào kỳ

vọng (suy từ notebook).

3. KIỂM TRA TRẠNG THÁI DỮ LIỆU (bắt buộc — nơi xử lý trạng

thái rỗng):

   - Chưa tải file →

`st.info` hướng dẫn + `st.stop()`.

   - Đã có file → nạp

dữ liệu qua hàm cache_data dùng chung, rồi `st.caption` xác nhận nguồn ("📁

Đang dùng tệp: <tên>").

4. (Tùy chọn) `st.caption` tóm tắt nhanh (số dòng / khoảng

thời gian / cột chính). KHÔNG đặt biểu đồ/bảng ở đây.

5. Phân tách với phần thân bằng `st.divider()`.

 

Quy tắc: header CHỈ trình bày + điều phối trạng thái rỗng/đã-có-dữ-liệu;

KHÔNG train, KHÔNG vẽ kết quả.

 

---

 

## THÀNH PHẦN 3: TAB "TỔNG QUAN DỮ LIỆU"

 

Cho người dùng nắm nhanh dữ liệu thô & đặc điểm thống kê

các biến của mô hình.

 

Nội dung:

1. KÍCH THƯỚC DỮ LIỆU: hàng `st.columns` + `st.metric`: số

dòng, số cột, dung lượng file (MB, từ file_uploader).

2. XEM DỮ LIỆU THÔ: `st.dataframe(df.head())` đặt trong

`st.container(height=...)` để cuộn gọn.

3. THỐNG KÊ MÔ TẢ: `st.dataframe(df[<biến của mô

hình>].describe())`. CHỈ mô tả các biến

   đưa vào mô hình (X và y nếu có) — đọc

notebook để biết tập biến — KHÔNG mô tả toàn bộ cột.

 

Quy tắc: tập biến lấy từ notebook; tab này chỉ cần dữ liệu

đã nạp, KHÔNG phụ thuộc train.

 

---

 

## THÀNH PHẦN 4: TAB "TRỰC QUAN HÓA DỮ LIỆU"

 

Trực quan hóa các biến đưa vào mô hình.

 

Nội dung:

1. THỨ TỰ ƯU TIÊN: bắt đầu bằng BIẾN MỤC TIÊU (y) nếu mô

hình có giám sát. Nếu KHÔNG có

   biến mục tiêu

(không giám sát / phát hiện bất thường), bắt đầu bằng biến đầu vào quan trọng

nhất.

2. TỰ CHỌN LOẠI BIỂU ĐỒ THEO KIỂU BIẾN (suy từ dtype):

   - Số liên tục →

histogram (hoặc box/violin xem ngoại lai).

   - Phân loại/rời rạc

→ bar theo value_counts.

   - Thời gian →

line/bar theo mốc thời gian.

   - Mục tiêu phân loại

→ bar phân phối lớp; mục tiêu liên tục → histogram.

3. BỐ TRÍ 4 BIỂU ĐỒ CÂN ĐỐI: lưới 2x2 (hai hàng

`st.columns(2)`), mục tiêu trước rồi các biến đầu vào.

4. NẾU QUÁ NHIỀU BIẾN (>4): thêm `st.multiselect` đầu tab

(mặc định 4 biến ưu tiên); vẽ theo lựa chọn.

 

Quy tắc: dùng plotly, `use_container_width=True`, chiều cao

cố định để cân đối; chọn biểu đồ

THEO kiểu dữ liệu thực tế (không gán cứng); chỉ cần dữ liệu

đã nạp. (Tùy chọn, Streamlit ≥1.55)

lazy-load biểu đồ nặng bằng dynamic container

(`on_change="rerun"` + `.open`).

 

---

 

## THÀNH PHẦN 5: TAB "KẾT QUẢ HUẤN LUYỆN & KIỂM ĐỊNH

MÔ HÌNH"

 

Hiển thị kết quả train & chỉ tiêu kiểm định ĐÚNG với loại

thuật toán đã chọn ở sidebar.

 

Điều phối: đọc kết quả từ `session_state`; nếu chưa train →

`st.info` hướng dẫn bấm nút & dừng tab.

 

Chọn chỉ tiêu theo HỌ THUẬT TOÁN (đọc notebook để xác định;

bám đúng những gì notebook đã tính nếu có):

- PHÂN LOẠI có giám sát → ma trận nhầm lẫn,

Accuracy/Precision/Recall/F1, ROC-AUC, classification report.

- HỒI QUY → R², RMSE, MAE, biểu đồ dự báo vs thực tế, biểu đồ

phần dư.

- PHÂN CỤM → Silhouette, kích thước từng cụm, scatter tô màu

theo cụm.

- PHÁT HIỆN BẤT THƯỜNG (IsolationForest/LOF/OneClassSVM) → số

& tỷ lệ bất thường,

  phân phối điểm bất

thường, scatter tô màu bất thường. (Chỉ tính precision/recall nếu có nhãn thực;

KHÔNG bịa nhãn.)

 

Trình bày: chỉ tiêu vô hướng → `st.columns` + `st.metric`;

ma trận/bảng → `st.dataframe`; biểu đồ → plotly.

 

---

 

## THÀNH PHẦN 6: TAB "SỬ DỤNG MÔ HÌNH"

 

Cho người dùng dùng MÔ HÌNH ĐÃ HUẤN LUYỆN để dự báo/chấm điểm

dữ liệu mới.

 

Điều phối: lấy mô hình đã fit + bộ tiền xử lý từ

`session_state`; nếu chưa train → hướng dẫn & dừng tab.

PHẢI áp dụng ĐÚNG cùng bộ tiền xử lý (scaler/encoder) như

lúc train.

 

Hai chế độ, chọn bằng `st.radio` ở đầu tab:

- CHẾ ĐỘ 1 — NHẬP TRỰC TIẾP: `st.form` bao một widget cho TỪNG

biến đầu vào X (số → number_input,

  mặc định = trung vị,

min/max theo dữ liệu; phân loại → selectbox theo giá trị có trong dữ liệu).

 `st.form_submit_button("Dự báo")` → tiền xử lý → dự báo → hiển

thị kết quả (`st.metric`/`st.success`,

  kèm xác suất/điểm số

nếu mô hình hỗ trợ).

- CHẾ ĐỘ 2 — TẢI FILE THEO CẤU TRÚC X_test:

`st.file_uploader` nhận file có ĐÚNG các cột biến đầu vào;

  kiểm tra schema (thiếu/thừa

cột → `st.error` liệt kê cột thiếu); dự báo hàng loạt → bảng kết quả

  (`st.dataframe`

trong container cuộn) → `st.download_button` xuất CSV (utf-8-sig).

 

Quy tắc: danh sách biến đầu vào/kiểu/khoảng lấy từ notebook

+ dữ liệu; KHÔNG train lại ở tab này.

Dưới đây là cấu trúc trọn vẹn và mã nguồn của 3 file cần thiết theo đúng đặc tả yêu cầu, được xây dựng dựa trên phân tích từ file notebook phát hiện giao dịch gian lận với tập dữ liệu đặc trưng các biến X_1 đến X_14 và biến mục tiêu default.

1. app.py
Python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import io

# 1) CONFIGURATION LÀ LỆNH STREAMLIT ĐẦU TIÊN
st.set_page_config(
    layout="wide",
    page_title="Hệ Thống Phát Hiện Giao Dịch Gian Lận",
    page_icon="🛡️"
)

# 2) HÀM NẠP DỮ LIỆU DÙNG CHUNG CÓ CACHE
@st.cache_data
def load_data(file_bytes, file_name):
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file dữ liệu: {e}")
        return None

# Cột đặc trưng mô hình yêu cầu cố định
MODEL_FEATURES = [f"X_{i}" for i in range(1, 15)]
TARGET_COL = "default"

# 3) SIDEBAR - VÙNG CẤU HÌNH
with st.sidebar:
    st.header("⚙️ Cấu hình & Tải dữ liệu")
    
    # Tải file dữ liệu huấn luyện mẫu
    uploaded_file = st.file_uploader(
        "Tải lên tệp dữ liệu huấn luyện mẫu", 
        type=["csv", "xlsx"],
        help="Hỗ trợ định dạng CSV hoặc Excel có chứa các cột X_1 đến X_14 và cột default"
    )
    
    st.divider()
    st.subheader("Tham số mô hình AI")
    st.caption("Mô hình: RandomForestClassifier")
    
    # Tham số chính trích xuất từ cấu hình notebook
    n_estimators = st.slider(
        "Số lượng cây quyết định (n_estimators)", 
        min_value=10, max_value=500, value=100, step=10,
        help="Số lượng cây phân loại ngẫu nhiên trong rừng."
    )
    
    random_state = st.number_input(
        "Trạng thái ngẫu nhiên (random_state)",
        min_value=0, max_value=9999, value=42, step=1,
        help="Đảm bảo tính tái lập của kết quả huấn luyện mô hình."
    )
    
    # Tham số nâng cao gom gọn trong expander
    with st.expander("🛠️ Cấu hình tham số nâng cao"):
        criterion = st.selectbox(
            "Tiêu chí phân tách (criterion)",
            options=["gini", "entropy", "log_loss"],
            index=0,
            help="Hàm đo lường chất lượng phép phân tách nhị phân."
        )
        max_depth = st.slider(
            "Độ sâu tối đa (max_depth)",
            min_value=2, max_value=50, value=15, step=1,
            help="Giới hạn chiều sâu tối đa của mỗi cây để tránh quá khớp (overfitting)."
        )
        min_samples_split = st.slider(
            "Mẫu tối thiểu để tách nút (min_samples_split)",
            min_value=2, max_value=20, value=2, step=1,
            help="Số lượng mẫu tối thiểu cần thiết để phân tách một nút nội bộ."
        )
        
    st.divider()
    
    # Nút bấm huấn luyện duy nhất kích hoạt dòng chảy
    train_clicked = st.button(
        "🚀 Huấn Luyện Mô Hình", 
        type="primary", 
        use_container_width=True,
        help="Bấm để bắt đầu phân tách dữ liệu, chạy pipeline tiền xử lý và fit mô hình Random Forest."
    )

# 4) HEADER - VÙNG ĐỊNH HƯỚNG MỤC TIÊU
st.title("🛡️ Ứng Dụng Phát Hiện Giao Dịch Gian Lận & Rủi Ro")
st.caption("Ứng dụng hỗ trợ phân tích hồ sơ giao dịch tài chính khách hàng, tự động phát hiện rủi ro tín dụng hoặc hành vi gian lận dựa trên học máy.")

if uploaded_file is None:
    st.info("💡 Vui lòng tải file dữ liệu mẫu (.csv / .xlsx) ở sidebar bên trái để bắt đầu phân tích.")
    st.stop()

# Đọc dữ liệu từ file bytes
file_bytes = uploaded_file.read()
df = load_data(file_bytes, uploaded_file.name)

if df is None:
    st.error("Tệp tải lên không hợp lệ hoặc bị lỗi định dạng. Vui lòng kiểm tra lại.")
    st.stop()

st.caption(f"📁 Đang dùng tệp: **{uploaded_file.name}** | Quy mô: **{df.shape[0]} dòng** và **{df.shape[1]} cột**.")
st.divider()

# 5) KHỐI XỬ LÝ TRAIN VÀ LƯU SESSION STATE KHI BẤM NÚT
if train_clicked:
    # Kiểm tra tính toàn vẹn của schema dữ liệu
    missing_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col not in df.columns]
    if missing_cols:
        st.error(f"Thiếu các cột bắt buộc trong file dữ liệu: {missing_cols}")
    else:
        with st.spinner("Đang huấn luyện mô hình... Vui lòng đợi trong giây lát..."):
            X = df[MODEL_FEATURES]
            y = df[TARGET_COL]
            
            # Tái hiện chuẩn xác quy trình phân chia dữ liệu từ notebook
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_split=0.2, random_value=random_state) if 'random_value' in locals() else train_test_split(X, y, test_size=0.2, random_state=random_state)
            
            # Cấu hình mô hình theo widget lựa chọn
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=random_state
            )
            model.fit(X_train, y_train)
            
            # Đánh giá kết quả kiểm định
            y_pred = model.predict(X_test)
            
            # Lưu trữ trạng thái vào session state
            st.session_state['trained_model'] = model
            st.session_state['features_list'] = MODEL_FEATURES
            st.session_state['eval_metrics'] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'confusion': confusion_matrix(y_test, y_pred),
                'report': classification_report(y_test, y_pred, output_dict=True)
            }
            st.success("🎉 Huấn luyện thành công mô hình! Kết quả đã được cập nhật ở các tab bên dưới.")

# 6) KHỐI TABS HIỂN THỊ NỘI DUNG CHÍNH
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tổng quan dữ liệu", 
    "📈 Trực quan hóa dữ liệu", 
    "🔬 Kết quả huấn luyện & Kiểm định", 
    "🔮 Sử dụng mô hình dự báo"
])

# --- TAB 1: TỔNG QUAN DỮ LIỆU ---
with tab1:
    st.subheader("Phân tích tổng quan dữ liệu thô")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Số lượng bản ghi (Dòng)", f"{df.shape[0]:,}")
    col_m2.metric("Số lượng trường thông tin (Cột)", df.shape[1])
    file_size_mb = len(file_bytes) / (1024 * 1024)
    col_m3.metric("Dung lượng tệp tin", f"{file_size_mb:.2f} MB")
    
    st.markdown("##### 5 dòng dữ liệu đầu tiên (Xem trước):")
    st.dataframe(df.head(5), use_container_width=True)
    
    st.markdown("##### Thống kê mô tả các biến đặc trưng đưa vào mô hình:")
    valid_desc_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col in df.columns]
    st.dataframe(df[valid_desc_cols].describe(), use_container_width=True)

# --- TAB 2: TRỰC QUAN HÓA DỮ LIỆU ---
with tab2:
    st.subheader("Biểu đồ trực quan hóa phân phối các biến")
    
    # Ưu tiên hiển thị biến mục tiêu 'default' phân phối lớp trước
    if TARGET_COL in df.columns:
        st.markdown("##### Phân phối của biến mục tiêu (default)")
        target_counts = df[TARGET_COL].value_counts().reset_index()
        target_counts.columns = [TARGET_COL, "Số lượng bản ghi"]
        target_counts[TARGET_COL] = target_counts[TARGET_COL].astype(str)
        fig_target = px.bar(target_counts, x=TARGET_COL, y="Số lượng bản ghi", color=TARGET_COL, 
                            title="Tỷ lệ phân bổ Giao dịch Bình thường (0) vs Gian lận/Rủi ro (1)",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_target, use_container_width=True)
    
    st.markdown("##### Phân phối của các biến đầu vào đặc trưng")
    # Lọc danh sách biến thực tế
    available_features = [col for col in MODEL_FEATURES if col in df.columns]
    
    # Hỗ trợ lựa chọn đa biến nếu có quá nhiều biến
    selected_vis_features = st.multiselect(
        "Chọn các biến đặc trưng muốn hiển thị đồ thị phân phối (Mặc định hiển thị 4 biến đầu tiên):",
        options=available_features,
        default=available_features[:4] if len(available_features) >= 4 else available_features
    )
    
    if selected_vis_features:
        # Tạo lưới biểu đồ cân đối tùy biến theo danh sách chọn
        num_selected = len(selected_vis_features)
        rows = (num_selected + 1) // 2
        
        for r in range(rows):
            cols = st.columns(2)
            for c in range(2):
                idx = r * 2 + c
                if idx < num_selected:
                    feature_name = selected_vis_features[idx]
                    fig_feat = px.histogram(df, x=feature_name, title=f"Biểu đồ phân phối của biến {feature_name}", 
                                            marginal="box", color_discrete_sequence=['#636EFA'])
                    fig_feat.update_layout(height=350)
                    cols[c].plotly_chart(fig_feat, use_container_width=True)
    else:
        st.warning("Vui lòng lựa chọn ít nhất một biến đặc trưng để hiển thị trực quan.")

# --- TAB 3: KẾT QUẢ HUẤN LUYỆN & KIỂM ĐỊNH MÔ HÌNH ---
with tab3:
    st.subheader("🔬 Chỉ số đánh giá và Ma trận nhầm lẫn")
    
    # Điều phối: Kiểm tra mô hình đã được huấn luyện chưa
    if 'trained_model' not in st.session_state:
        st.info("💡 Mô hình chưa được kích hoạt huấn luyện. Vui lòng chuyển cấu hình tham số và nhấn nút 'Huấn Luyện Mô Hình' ở sidebar bên trái.")
    else:
        metrics = st.session_state['eval_metrics']
        
        # Hiển thị chỉ tiêu vô hướng qua metric cards
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        col_c1.metric("Độ chính xác toàn cục (Accuracy)", f"{metrics['accuracy']:.4f}")
        col_c2.metric("Độ chính xác mô hình (Precision)", f"{metrics['precision']:.4f}")
        col_c3.metric("Tỷ lệ tìm sót lỗi (Recall)", f"{metrics['recall']:.4f}")
        col_c4.metric("Chỉ số cân bằng (F1-Score)", f"{metrics['f1']:.4f}")
        
        st.divider()
        
        col_l, col_r = st.columns(2)
        
        with col_l:
            st.markdown("##### Ma trận nhầm lẫn (Confusion Matrix):")
            cm = metrics['confusion']
            cm_df = pd.DataFrame(cm, index=['Thực tế: Thường (0)', 'Thực tế: Gian lận (1)'], 
                                 columns=['Dự đoán: Thường (0)', 'Dự đoán: Gian lận (1)'])
            st.dataframe(cm_df, use_container_width=True)
            
            # Biểu diễn Heatmap trực quan cho trực diện bằng Plotly
            fig_cm = px.imshow(cm, text_auto=True, 
                               labels=dict(x="Nhãn Dự Đoán", y="Nhãn Thực Tế"),
                               x=['Bình thường (0)', 'Gian lận (1)'],
                               y=['Bình thường (0)', 'Gian lận (1)'],
                               color_continuous_scale='Blues', title="Heatmap Confusion Matrix")
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with col_r:
            st.markdown("##### Báo cáo chi tiết (Classification Report):")
            report_df = pd.DataFrame(metrics['report']).transpose()
            st.dataframe(report_df.style.format(precision=4), use_container_width=True)
            
            # Hiển thị mức độ quan trọng của các đặc trưng (Feature Importance)
            st.markdown("##### Độ quan trọng của các biến đầu vào:")
            importances = st.session_state['trained_model'].feature_importances_
            feat_imp_df = pd.DataFrame({
                'Đặc trưng': st.session_state['features_list'],
                'Độ quan trọng': importances
            }).sort_values(by='Độ quan trọng', ascending=True)
            
            fig_imp = px.bar(feat_imp_df, x='Độ quan trọng', y='Đặc trưng', orientation='h',
                             title='Biểu đồ sắp xếp độ quan trọng đặc trưng (Feature Importances)',
                             color='Độ quan trọng', color_continuous_scale='Viridis')
            fig_imp.update_layout(height=400)
            st.plotly_chart(fig_imp, use_container_width=True)

# --- TAB 4: SỬ DỤNG MÔ HÌNH DỰ BÁO ---
with tab4:
    st.subheader("🔮 Chẩn đoán xác suất rủi ro giao dịch mới")
    
    if 'trained_model' not in st.session_state:
        st.info("💡 Vui lòng thực hiện bước huấn luyện mô hình thành công tại sidebar trước khi thực hiện dự đoán rủi ro mới.")
    else:
        model = st.session_state['trained_model']
        
        predict_mode = st.radio(
            "Lựa chọn phương thức nhập dữ liệu mới cần kiểm tra:",
            options=["Nhập thông số trực tiếp qua Form", "Tải tệp danh sách hồ sơ kiểm tra hàng loạt (.csv / .xlsx)"],
            horizontal=True
        )
        
        if predict_mode == "Nhập thông số trực tiếp qua Form":
            st.markdown("##### Điền các thông số kỹ thuật của giao dịch đơn lẻ:")
            
            # Tạo form nhập liệu cho 14 biến, tự lấy trung vị làm mặc định bảo toàn an toàn hệ thống
            with st.form("single_prediction_form"):
                inputs = {}
                # Chia form thành 2 cột cho giao diện cân đối, gọn gàng
                col_f1, col_f2 = st.columns(2)
                
                for idx, feat in enumerate(MODEL_FEATURES):
                    # Lấy min, max, median từ tệp dữ liệu huấn luyện để gợi ý khoảng hợp lý cho người dùng
                    if feat in df.columns:
                        min_v = float(df[feat].min())
                        max_v = float(df[feat].max())
                        mean_v = float(df[feat].median())
                    else:
                        min_v, max_v, mean_v = -10.0, 10.0, 0.0
                        
                    with col_f1 if idx % 2 == 0 else col_f2:
                        inputs[feat] = st.number_input(
                            f"Thông số {feat}",
                            min_value=min_v*2.0, max_value=max_v*2.0, value=mean_v, format="%.6f",
                            help=f"Nhập giá trị định lượng cho biến {feat} (Khoảng mẫu: {min_v:.2f} đến {max_v:.2f})"
                        )
                
                submit_pred = st.form_submit_button("Chẩn đoán Giao Dịch", type="primary", use_container_width=True)
                
            if submit_pred:
                input_df = pd.DataFrame([inputs])
                # Đảm bảo thứ tự các cột chính xác như lúc huấn luyện
                input_df = input_df[MODEL_FEATURES]
                
                prediction = model.predict(input_df)[0]
                probabilities = model.predict_proba(input_df)[0]
                
                st.markdown("---")
                st.markdown("##### Kết quả phân tích chẩn đoán giao dịch:")
                
                col_r1, col_r2 = st.columns(2)
                
                if prediction == 1:
                    col_r1.error("⚠️ CẢNH BÁO: Giao dịch có dấu hiệu GIAN LẬN / RỦI RO CAO")
                    col_r2.metric("Xác suất rủi ro phát hiện", f"{probabilities[1]*100:.2f} %")
                else:
                    col_r1.success("✅ AN TOÀN: Giao dịch bình thường, độ tin cậy đạt yêu cầu")
                    col_r2.metric("Xác suất an toàn", f"{probabilities[0]*100:.2f} %")
                    
        elif predict_mode == "Tải tệp danh sách hồ sơ kiểm tra hàng loạt (.csv / .xlsx)":
            st.markdown("##### Tải lên tệp chứa danh sách các giao dịch mới cần quét rủi ro đồng loạt:")
            st.caption("Yêu cầu cấu trúc: Tệp tải lên bắt buộc phải chứa đầy đủ 14 cột đặc trưng từ `X_1` đến `X_14`.")
            
            new_file_uploader = st.file_uploader("Tải tệp kiểm tra rủi ro hàng loạt", type=["csv", "xlsx"], key="batch_uploader")
            
            if new_file_uploader is not None:
                new_bytes = new_file_uploader.read()
                df_new = load_data(new_bytes, new_file_uploader.name)
                
                if df_new is not None:
                    # Kiểm tra schema hợp lệ
                    missing_batch_cols = [col for col in MODEL_FEATURES if col not in df_new.columns]
                    if missing_batch_cols:
                        st.error(f"Đọc file thất bại! Tệp tải lên thiếu các cột biến đặc trưng sau: {missing_batch_cols}")
                    else:
                        X_new_payload = df_new[MODEL_FEATURES]
                        
                        # Dự báo hàng loạt
                        batch_predictions = model.predict(X_new_payload)
                        batch_probs = model.predict_proba(X_new_payload)[:, 1] # Xác suất lớp 1 (gian lận)
                        
                        # Đính kèm thêm kết quả vào bảng dữ liệu xuất ra
                        df_result = df_new.copy()
                        df_result['Du_bao_Rui_Ro'] = batch_predictions
                        df_result['Xac_Suat_Gian_Lan'] = batch_probs
                        
                        st.success(f"Quét dữ liệu hoàn tất! Đã dự báo xong cho hoàn chỉnh {df_new.shape[0]} giao dịch.")
                        
                        # Thống kê tổng quan rủi ro lô giao dịch
                        num_frauds = int(np.sum(batch_predictions))
                        st.warning(f"🚨 Phát hiện **{num_frauds}** giao dịch tiềm ẩn rủi ro cao trên tổng số **{df_new.shape[0]}** giao dịch vừa nạp.")
                        
                        st.markdown("##### Bảng kết quả tổng hợp chi tiết dự báo hàng loạt:")
                        st.dataframe(df_result, use_container_width=True)
                        
                        # Chuẩn bị file tải về cho người dùng cuối
                        csv_buffer = io.StringIO()
                        df_result.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                        csv_data = csv_buffer.getvalue()
                        
                        st.download_button(
                            label="📥 Tải xuống bảng kết quả dự báo dạng CSV",
                            data=csv_data,
                            file_name="ket_qua_du_bao_gian_lan_hang_loat.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
2. requirements.txt
Plaintext
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.2.0
plotly>=5.15.0
openpyxl>=3.1.0
3. README.md
Markdown
# 🛡️ Ứng dụng Học Máy Phát Hiện Giao Dịch Gian Lận & Rủi Ro Tín Dụng

Ứng dụng web được xây dựng hoàn toàn bằng thư viện **Streamlit** (Python), giúp chuyển đổi quy trình huấn luyện từ Notebook sang giao diện web trực quan, cho phép người dùng cấu hình tham số, huấn luyện mô hình **RandomForestClassifier** trong thời gian thực và tiến hành dự đoán rủi ro cho các hồ sơ giao dịch mới.

---

## 🧭 Kiến trúc Phân vùng Giao diện (Layout Zoning)

Ứng dụng được thiết kế tối ưu theo các nguyên tắc phân vùng tốt nhất của Streamlit:
* **Vùng Cấu hình cố định (Sidebar):** Nơi tiếp nhận tệp dữ liệu mẫu huấn luyện đầu vào, cho phép tùy chỉnh linh hoạt các tham số của thuật toán Random Forest và nút bấm kích hoạt huấn luyện duy nhất.
* **Vùng chính (Main Page):** Bao gồm tiêu đề định hướng thông tin, kiểm tra ranh giới trạng thái rỗng của tập dữ liệu và phân tách nội dung thành 4 tab chức năng thông minh độc lập không gây hiện tượng chạy lại huấn luyện (rerun) thừa thãi.

---

## 📊 Mô tả Tóm Tắt các Tab Chức Năng

1.  **📊 Tổng quan dữ liệu:** Hiển thị kích thước dữ liệu tổng quát, thống kê mô tả phân phối tập trung (`describe`) và bảng dữ liệu xem trước 5 dòng đầu của hệ thống.
2.  **📈 Trực quan hóa dữ liệu:** Sử dụng thư viện đồ thị tương tác cao **Plotly**, ưu tiên hiển thị biểu đồ tần suất phân phối của biến mục tiêu `default` sau đó là lưới biểu đồ phân phối động của các biến đầu vào (`X_1` tới `X_14`).
3.  **🔬 Kết quả huấn luyện & Kiểm định:** Cung cấp các chỉ số đánh giá cốt lõi: *Accuracy, Precision, Recall, F1-Score*. Đồng thời hiển thị biểu đồ Heatmap Ma trận nhầm lẫn (Confusion Matrix) và Đồ thị sắp xếp mức độ quan trọng đặc trưng của các biến.
4.  **🔮 Sử dụng mô hình dự báo:** * *Chế độ nhập trực tiếp:* Cung cấp Form giao diện nhập nhanh thông số của 1 bản ghi với gợi ý mặc định là giá trị trung vị an toàn.
    * *Chế độ tải file hàng loạt:* Nhận tệp chứa danh sách nhiều giao dịch mới, tự động kiểm tra đối chiếu schema cấu trúc cột và cho phép xuất tệp kết quả dự đoán kèm xác suất rủi ro định lượng.

---

## 📁 Cấu Trúc File Dữ Liệu Đầu Vào Yêu Cầu

Để ứng dụng vận hành chính xác và tránh lỗi hệ thống, tệp dữ liệu của bạn cần tuân thủ cấu trúc sau:
* **Định dạng file:** `.csv`, `.xlsx`, hoặc `.xls`.
* **Danh sách các cột biến độc lập (X):** Bao gồm đúng 14 cột mang tên từ `X_1`, `X_2`, `X_3`, ..., cho đến `X_14` chứa dữ liệu dạng số (liên tục hoặc rời rạc).
* **Cột biến mục tiêu phụ thuộc (y):** Cột mang tên `default` nhận hai giá trị phân loại nhị phân chính: `0` (Giao dịch bình thường) và `1` (Giao dịch gian lận hoặc rủi ro cao).

---

## 🛠️ Hướng dẫn Cài đặt & Khởi chạy ứng dụng

### 1. Chuẩn bị môi trường
Khuyến nghị sử dụng Python phiên bản từ **3.9 đến 3.12**. Tạo một môi trường ảo độc lập (Virtual Environment) để tránh xung đột thư viện:
```bash
# Tạo môi trường ảo mới
python -m venv venv

# Kích hoạt môi trường ảo (Hệ điều hành Windows)
venv\Scripts\activate

# Kích hoạt môi trường ảo (Hệ điều hành macOS/Linux)
source venv/bin/activate
2. Cài đặt các thư viện phụ thuộc bắt buộc
Cài đặt tất cả các gói package thông qua file cấu hình đính kèm:

Bash
pip install -r requirements.txt
3. Khởi chạy Web App Streamlit
Thực hiện lệnh điều hướng khởi chạy máy chủ cục bộ:

Bash
streamlit run app.py
Sau khi chạy lệnh thành công, hệ thống sẽ tự động mở trình duyệt web mặc định của bạn tại địa chỉ mặc định http://localhost:8501.

📝 Ghi Chú Kỹ Thuật Hệ Thống
Quản lý trạng thái thông minh: Trình nạp dữ liệu sử dụng decorator @st.cache_data truyền dạng byte an toàn để tối ưu bộ nhớ. Toàn bộ các đối tượng mô hình sau huấn luyện, bộ chỉ số đo lường đều được quản lý tập trung thông qua đối tượng st.session_state giúp tối ưu hóa hiệu năng phần cứng và nâng cao trải nghiệm người dùng cuối.

Viết lại để có thể chọn thuật toán huấn luyện Random Forest, Decision tree, LogisticRegression

Dưới đây là mã nguồn toàn diện của 3 file (app.py, requirements.txt, README.md) đã được cập nhật để tích hợp linh hoạt 3 thuật toán: Random Forest, Decision Tree và Logistic Regression, hỗ trợ thay đổi tham số động theo từng mô hình và lưu trữ trạng thái đồng bộ.

1. app.py
Python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import io

# 1) CONFIGURATION LÀ LỆNH STREAMLIT ĐẦU TIÊN
st.set_page_config(
    layout="wide",
    page_title="Hệ Thống Chẩn Đoán Giao Dịch Rủi Ro",
    page_icon="🛡️"
)

# 2) HÀM NẠP DỮ LIỆU DÙNG CHUNG CÓ CACHE
@st.cache_data
def load_data(file_bytes, file_name):
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file dữ liệu: {e}")
        return None

# Định nghĩa tập biến đầu vào X và biến mục tiêu y từ thiết kế hệ thống
MODEL_FEATURES = [f"X_{i}" for i in range(1, 15)]
TARGET_COL = "default"

# 3) SIDEBAR - VÙNG CẤU HÌNH DỮ LIỆU & THAM SỐ ĐỘNG
with st.sidebar:
    st.header("⚙️ Cấu hình & Tải dữ liệu")
    
    # Nạp file mẫu
    uploaded_file = st.file_uploader(
        "Tải lên tệp dữ liệu mẫu", 
        type=["csv", "xlsx"],
        help="Hỗ trợ định dạng CSV hoặc Excel chứa các cột X_1 đến X_14 và cột mục tiêu default"
    )
    
    st.divider()
    st.subheader("🤖 Lựa chọn Mô hình")
    
    # Hộp chọn thuật toán huấn luyện
    model_choice = st.selectbox(
        "Thuật toán huấn luyện:",
        options=["Random Forest", "Decision Tree", "Logistic Regression"],
        index=0,
        help="Chọn thuật toán học máy phù hợp để phân tích và phân loại rủi ro giao dịch."
    )
    
    st.divider()
    st.subheader("🎛️ Tham số mô hình AI")
    
    # Thiết lập giao diện tham số động (Dynamic UI) dựa trên mô hình được chọn
    params = {}
    
    if model_choice == "Random Forest":
        params['n_estimators'] = st.slider(
            "Số lượng cây (n_estimators)", 
            min_value=10, max_value=500, value=100, step=10,
            help="Số lượng cây quyết định phối hợp ngẫu nhiên trong rừng."
        )
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['criterion'] = st.selectbox("Tiêu chí phân tách (criterion)", ["gini", "entropy", "log_loss"], index=0)
            params['max_depth'] = st.slider("Độ sâu tối đa (max_depth)", 2, 50, 15)
            params['min_samples_split'] = st.slider("Mẫu tối thiểu để tách nút", 2, 20, 2)
            
    elif model_choice == "Decision Tree":
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['criterion'] = st.selectbox("Tiêu chí phân tách (criterion)", ["gini", "entropy", "log_loss"], index=0)
            params['max_depth'] = st.slider("Độ sâu tối đa (max_depth)", 2, 50, 10)
            params['min_samples_split'] = st.slider("Mẫu tối thiểu để tách nút", 2, 20, 2)
            
    elif model_choice == "Logistic Regression":
        params['max_iter'] = st.slider(
            "Số vòng lặp tối đa (max_iter)",
            min_value=100, max_value=2000, value=1000, step=100,
            help="Số lượng vòng lặp tối đa cho các thuật toán tối ưu hội tụ."
        )
        params['C'] = st.number_input(
            "Hệ số nghịch đảo chính quy hóa (C)",
            min_value=0.001, max_value=100.0, value=1.0, step=0.1, format="%.3f",
            help="Giá trị C càng nhỏ thì mức độ chính quy hóa (regularization) càng mạnh nhằm giảm quá khớp."
        )
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['penalty'] = st.selectbox("Phương thức phạt (penalty)", ["l2", None], index=0)
            params['solver'] = st.selectbox("Thuật toán tối ưu (solver)", ["lbfgs", "newton-cg", "saga"], index=0)

    st.divider()
    
    # Nút thực hiện tác vụ huấn luyện duy nhất đặt ở dưới cùng
    train_clicked = st.button(
        "🚀 Huấn Luyện Mô Hình", 
        type="primary", 
        use_container_width=True,
        help="Nhấp để chia dữ liệu Train/Test và huấn luyện thuật toán đang được lựa chọn."
    )

# 4) HEADER - VÙNG ĐỊNH HƯỚNG TRẠNG THÁI
st.title("🛡️ Ứng Dụng Phát Hiện Giao Dịch Gian Lận & Rủi Ro")
st.caption("Giao diện phân tích đa mô hình học máy: Hỗ trợ đánh giá, so sánh hiệu năng thuật toán và chấm điểm hồ sơ tài chính.")

if uploaded_file is None:
    st.info("💡 Hệ thống đang trống dữ liệu. Vui lòng tải file mẫu (.csv / .xlsx) tại Sidebar bên trái để tiếp tục.")
    st.stop()

# Đọc dữ liệu thô thông qua hàm cache
file_bytes = uploaded_file.read()
df = load_data(file_bytes, uploaded_file.name)

if df is None:
    st.error("Lỗi: Không thể phân tích cú pháp tệp dữ liệu đã tải lên.")
    st.stop()

st.caption(f"📁 Đang kết nối tệp: **{uploaded_file.name}** | Kích thước: **{df.shape[0]} dòng** × **{df.shape[1]} cột**.")
st.divider()

# 5) KHỐI XỬ LÝ TRAIN VÀ LƯU SESSION STATE KHI BẤM NÚT
if train_clicked:
    missing_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col not in df.columns]
    if missing_cols:
        st.error(f"D dữ liệu tải lên không hợp lệ, thiếu các trường quan trọng: {missing_cols}")
    else:
        with st.spinner(f"Đang tiến hành huấn luyện thuật toán {model_choice}..."):
            X = df[MODEL_FEATURES]
            y = df[TARGET_COL]
            
            # Phân tách tập dữ liệu với tỷ lệ mẫu test 20%
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=params['random_state'])
            
            # Khởi tạo thuật toán dựa theo cấu hình động
            if model_choice == "Random Forest":
                model = RandomForestClassifier(
                    n_estimators=params['n_estimators'],
                    criterion=params['criterion'],
                    max_depth=params['max_depth'],
                    min_samples_split=params['min_samples_split'],
                    random_state=params['random_state']
                )
            elif model_choice == "Decision Tree":
                model = DecisionTreeClassifier(
                    criterion=params['criterion'],
                    max_depth=params['max_depth'],
                    min_samples_split=params['min_samples_split'],
                    random_state=params['random_state']
                )
            elif model_choice == "Logistic Regression":
                model = LogisticRegression(
                    max_iter=params['max_iter'],
                    C=params['C'],
                    penalty=params['penalty'],
                    solver=params['solver'],
                    random_state=params['random_state']
                )
                
            # Thực thi huấn luyện pipeline
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Đóng gói và lưu trữ đồng bộ vào Session State để các Tab dùng chung không bị mất dữ liệu
            st.session_state['active_model'] = model
            st.session_state['model_type'] = model_choice
            st.session_state['trained_features'] = MODEL_FEATURES
            st.session_state['metrics_results'] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'confusion': confusion_matrix(y_test, y_pred),
                'report': classification_report(y_test, y_pred, output_dict=True)
            }
            st.success(f"🎉 Đã hoàn tất huấn luyện mô hình **{model_choice}** thành công!")

# 6) PHÂN CHIA TABS HIỂN THỊ KẾT QUẢ VÀ NGHIỆP VỤ
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Phân Tích Tổng Quan", 
    "📈 Trực Quan Hóa Biến", 
    "🔬 Kiểm Định & Đánh Giá", 
    "🔮 Ứng Dụng Chẩn Đoán"
])

# --- TAB 1: PHÂN TÍCH TỔNG QUAN ---
with tab1:
    st.subheader("Đặc trưng và Thống kê Dữ liệu Huấn luyện")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng số bản ghi", f"{df.shape[0]:,}")
    col_m2.metric("Số lượng cột thuộc tính", df.shape[1])
    col_m3.metric("Dung lượng file", f"{(len(file_bytes)/(1024*1024)):.2f} MB")
    
    st.markdown("##### Bản xem trước dữ liệu mẫu (5 dòng đầu):")
    st.dataframe(df.head(5), use_container_width=True)
    
    st.markdown("##### Thống kê mô tả toán học của các biến đặc trưng:")
    active_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col in df.columns]
    st.dataframe(df[active_cols].describe(), use_container_width=True)

# --- TAB 2: TRỰC QUAN HÓA BIẾN ---
with tab2:
    st.subheader("Biểu đồ Phân Phối Tần Suất Đặc Trưng")
    
    if TARGET_COL in df.columns:
        st.markdown("##### 1. Tỷ lệ phân bổ biến mục tiêu rủi ro (`default`)")
        target_data = df[TARGET_COL].value_counts().reset_index()
        target_data.columns = [TARGET_COL, "Số lượng"]
        target_data[TARGET_COL] = target_data[TARGET_COL].astype(str).map({'0': '0 (Bình thường)', '1': '1 (Rủi ro/Gian lận)'})
        
        fig_target = px.bar(target_data, x=TARGET_COL, y="Số lượng", color=TARGET_COL,
                            color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_target, use_container_width=True)
        
    st.markdown("##### 2. Biểu đồ phân phối chi tiết các biến đầu vào X")
    valid_features = [col for col in MODEL_FEATURES if col in df.columns]
    
    selected_features = st.multiselect(
        "Tùy chọn hiển thị đồ thị (Tối đa hiển thị lưới 4 biến mặc định):",
        options=valid_features,
        default=valid_features[:4] if len(valid_features) >= 4 else valid_features
    )
    
    if selected_features:
        n_selected = len(selected_features)
        n_rows = (n_selected + 1) // 2
        for r in range(n_rows):
            grid_cols = st.columns(2)
            for c in range(2):
                f_idx = r * 2 + c
                if f_idx < n_selected:
                    feat_name = selected_features[f_idx]
                    fig_h = px.histogram(df, x=feat_name, title=f"Phân phối của {feat_name}", marginal="box")
                    fig_h.update_layout(height=350)
                    grid_cols[c].plotly_chart(fig_h, use_container_width=True)
    else:
        st.warning("Vui lòng chọn tối thiểu một trường thông tin để vẽ biểu đồ.")

# --- TAB 3: KIỂM ĐỊNH & ĐÁNH GIÁ MÔ HÌNH ---
with tab3:
    if 'active_model' not in st.session_state:
        st.info("💡 Hệ thống chưa có dữ liệu kiểm định. Vui lòng chọn tham số mô hình và nhấn nút 'Huấn Luyện Mô Hình' tại Sidebar.")
    else:
        current_model_type = st.session_state['model_type']
        metrics = st.session_state['metrics_results']
        
        st.subheader(f"🔬 Kết Quả Kiểm Định Thuật Toán: {current_model_type}")
        
        # Hiển thị các chỉ số cốt lõi
        c_1, c_2, c_3, c_4 = st.columns(4)
        c_1.metric("Độ chính xác (Accuracy)", f"{metrics['accuracy']:.4f}")
        c_2.metric("Độ chính xác lớp 1 (Precision)", f"{metrics['precision']:.4f}")
        c_3.metric("Độ bao phủ/Nhớ sót (Recall)", f"{metrics['recall']:.4f}")
        c_4.metric("Chỉ số cân bằng F1", f"{metrics['f1']:.4f}")
        
        st.divider()
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("##### Ma trận nhầm lẫn (Confusion Matrix)")
            cm = metrics['confusion']
            cm_dataframe = pd.DataFrame(cm, index=['Thực tế: Thường (0)', 'Thực tế: Rủi ro (1)'],
                                        columns=['Dự đoán: Thường (0)', 'Dự đoán: Rủi ro (1)'])
            st.dataframe(cm_dataframe, use_container_width=True)
            
            fig_matrix = px.imshow(cm, text_auto=True, x=['Thường (0)', 'Rủi ro (1)'], y=['Thường (0)', 'Rủi ro (1)'],
                                   color_continuous_scale='Purples', title="Heatmap Ma Trận Nhầm Lẫn")
            st.plotly_chart(fig_matrix, use_container_width=True)
            
        with col_right:
            st.markdown("##### Báo cáo phân loại chi tiết (Classification Report)")
            rep_df = pd.DataFrame(metrics['report']).transpose()
            st.dataframe(rep_df.style.format(precision=4), use_container_width=True)
            
            # Hiển thị Mức độ quan trọng hoặc Hệ số hồi quy tùy thuộc vào thuật toán
            active_model_obj = st.session_state['active_model']
            
            if hasattr(active_model_obj, 'feature_importances_'):
                st.markdown("##### Mức độ đóng góp của các biến (Feature Importance):")
                importances = active_model_obj.feature_importances_
                imp_df = pd.DataFrame({'Đặc trưng': st.session_state['trained_features'], 'Trọng số': importances}).sort_values(by='Trọng số', ascending=True)
                fig_i = px.bar(imp_df, x='Trọng số', y='Đặc trưng', orientation='h', color='Trọng số', color_continuous_scale='teal')
                fig_i.update_layout(height=350)
                st.plotly_chart(fig_i, use_container_width=True)
                
            elif hasattr(active_model_obj, 'coef_'):
                st.markdown("##### Hệ số hồi quy tuyến tính (Model Coefficients):")
                coefficients = active_model_obj.coef_[0]
                coef_df = pd.DataFrame({'Đặc trưng': st.session_state['trained_features'], 'Hệ số hồi quy': coefficients}).sort_values(by='Hệ số hồi quy')
                fig_c = px.bar(coef_df, x='Hệ số hồi quy', y='Đặc trưng', orientation='h', color='Hệ số hồi quy', color_continuous_scale='RdBu_r')
                fig_c.update_layout(height=350)
                st.plotly_chart(fig_c, use_container_width=True)

# --- TAB 4: ỨNG DỤNG CHẨN ĐOÁN DỮ LIỆU MỚI ---
with tab4:
    if 'active_model' not in st.session_state:
        st.info("💡 Vui lòng kích hoạt huấn luyện mô hình ở cấu hình trước khi sử dụng tính năng dự đoán rủi ro.")
    else:
        active_model_obj = st.session_state['active_model']
        
        mode = st.radio(
            "Chọn chế độ nạp hồ sơ giao dịch mới cần kiểm thử:",
            options=["Chẩn đoán hồ sơ đơn lẻ (Form nhập trực tiếp)", "Dự đoán hàng loạt theo danh sách (Upload File Tệp)"],
            horizontal=True
        )
        
        if mode == "Chẩn đoán hồ sơ đơn lẻ (Form nhập trực tiếp)":
            st.markdown("##### Điền các thông số kỹ thuật số đo giao dịch hiện hành:")
            
            with st.form("form_single_predict"):
                form_inputs = {}
                f_col1, f_col2 = st.columns(2)
                
                for idx, col_feat in enumerate(MODEL_FEATURES):
                    # Khởi tạo giá trị mặc định bằng trung vị mẫu huấn luyện nhằm đảm bảo logic nghiệp vụ
                    if col_feat in df.columns:
                        v_min = float(df[col_feat].min())
                        v_max = float(df[col_feat].max())
                        v_med = float(df[col_feat].median())
                    else:
                        v_min, v_max, v_med = -5.0, 5.0, 0.0
                        
                    with f_col1 if idx % 2 == 0 else f_col2:
                        form_inputs[col_feat] = st.number_input(
                            f"Giá trị thông số {col_feat}",
                            min_value=v_min*3.0, max_value=v_max*3.0, value=v_med, format="%.6f",
                            help=f"Khoảng giá trị mẫu huấn luyện: [{v_min:.2f}, {v_max:.2f}]"
                        )
                        
                btn_diagnose = st.form_submit_button("Tiến Hành Chẩn Đoán", type="primary", use_container_width=True)
                
            if btn_diagnose:
                single_payload = pd.DataFrame([form_inputs])[MODEL_FEATURES]
                pred_label = active_model_obj.predict(single_payload)[0]
                
                st.markdown("---")
                st.markdown("##### Kết luận chẩn đoán hệ thống:")
                
                res_col1, res_col2 = st.columns(2)
                if pred_label == 1:
                    res_col1.error("⚠️ CẢNH BÁO NGUY HIỂM: Giao dịch có dấu hiệu bất thường / Rủi ro cao.")
                else:
                    res_col1.success("✅ HỆ THỐNG AN TOÀN: Giao dịch có chỉ số bình thường, độ tin cậy cao.")
                    
                if hasattr(active_model_obj, "predict_proba"):
                    probs = active_model_obj.predict_proba(single_payload)[0]
                    res_col2.metric("Xác suất phân loại rủi ro (Lớp 1)", f"{probs[1]*100:.2f} %")
                    res_col2.progress(float(probs[1]))
                    
        elif mode == "Dự đoán hàng loạt theo danh sách (Upload File Tệp)":
            st.markdown("##### Quét kiểm tra danh sách rủi ro đồng loạt bằng Tệp tin:")
            st.caption("Yêu cầu định dạng cấu trúc tệp: Tệp tải lên phải chứa đầy đủ cấu trúc tên cột từ `X_1` tới `X_14`.")
            
            bulk_file = st.file_uploader("Nạp tệp Excel/CSV danh sách cần quét:", type=["csv", "xlsx"], key="bulk_key")
            
            if bulk_file is not None:
                bulk_bytes = bulk_file.read()
                df_bulk = load_data(bulk_bytes, bulk_file.name)
                
                if df_bulk is not None:
                    missing_bulk = [c for c in MODEL_FEATURES if c not in df_bulk.columns]
                    if missing_bulk:
                        st.error(f"Quét file thất bại! Thiếu các cột biến đầu vào sau trong cấu trúc file nạp: {missing_bulk}")
                    else:
                        bulk_payload = df_bulk[MODEL_FEATURES]
                        predictions = active_model_obj.predict(bulk_payload)
                        
                        df_output = df_bulk.copy()
                        df_output['Du_Bao_Rui_Ro'] = predictions
                        
                        if hasattr(active_model_obj, "predict_proba"):
                            df_output['Xac_Suat_Rui_Ro'] = active_model_obj.predict_proba(bulk_payload)[:, 1]
                            
                        st.success(f"Xử lý hoàn tất! Đã chấm điểm rủi ro tự động cho {df_bulk.shape[0]} giao dịch thành công.")
                        
                        total_alerts = int(np.sum(predictions))
                        st.warning(f"🚨 Phát hiện chỉ dấu rủi ro tại **{total_alerts}** dòng hồ sơ giao dịch bất thường.")
                        
                        st.markdown("##### Bảng theo dõi kết quả quét hàng loạt:")
                        st.dataframe(df_output, use_container_width=True)
                        
                        # Xuất dữ liệu tải về dưới dạng CSV tiêu chuẩn mã hóa utf-8-sig
                        buffer_csv = io.StringIO()
                        df_output.to_csv(buffer_csv, index=False, encoding='utf-8-sig')
                        csv_payload_string = buffer_csv.getvalue()
                        
                        st.download_button(
                            label="📥 Tải Xuống Bảng Kết Quả Định Giá (.CSV)",
                            data=csv_payload_string,
                            file_name="ket_qua_quet_rui_ro_giao_dich.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
2. requirements.txt
Plaintext
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.2.0
plotly>=5.15.0
openpyxl>=3.1.0
3. README.md
Markdown
# 🛡️ Ứng dụng Phân Tích & Chẩn Đoán Giao Dịch Rủi Ro Đa Mô Hình Học Máy

Ứng dụng web được phát triển bằng nền tảng **Streamlit** (Python), giúp chuyển đổi các quy trình nghiên cứu cấu trúc dữ liệu mô hình từ Notebook thành một công cụ vận hành thực tế trực quan. Ứng dụng tích hợp đồng thời 3 mô hình phân loại lõi: **Random Forest**, **Decision Tree**, và **Logistic Regression**.

---

## 🏗️ Nguyên Tắc Thiết Kế Giao Diện & Luồng Xử Lý (Layout Zoning)

Giao diện ứng dụng tuân thủ nghiêm ngặt mô hình phân vùng trải nghiệm người dùng:
1. **Thanh Sidebar (Vùng cấu hình):** Tiếp nhận dữ liệu huấn luyện mẫu ban đầu, lựa chọn thuật toán thông minh và tự động thay đổi các widget cấu hình tham số tương ứng theo từng mô hình, đi kèm nút bấm kích hoạt huấn luyện duy nhất.
2. **Vùng chính (Main Screen):** Kiểm soát luồng logic biên trạng thái rỗng và hiển thị hệ thống 4 nhóm Tab tách biệt giúp giữ trạng thái mô hình ổn định mà không bị chạy lại (rerun) mô hình khi tương tác:
   * **📊 Phân Tích Tổng Quan:** Đọc và mô tả toán học tổng quan các chỉ số phân phối tập trung của dữ liệu thô.
   * **📈 Trực Quan Hóa Biến:** Sử dụng biểu đồ động **Plotly** hiển thị phân phối lớp mất cân bằng của biến mục tiêu `default` và cấu trúc các biến độc lập `X_1` -> `X_14`.
   * **🔬 Kiểm Định & Đánh Giá:** Tái hiện chi tiết các độ đo đánh giá mô hình học máy gồm *Accuracy, Precision, Recall, F1-score*, biểu diễn Heatmap ma trận nhầm lẫn và biểu đồ mức độ đóng góp thuộc tính (*Feature Importance* cho Rừng/Cây quyết định hoặc *Coefficients* cho Hồi quy Logistic).
   * **🔮 Ứng Dụng Chẩn Đoán:** Cung cấp tính năng dự báo hồ sơ đơn lẻ qua Form nhập liệu an toàn hoặc quét nhận định rủi ro tự động hàng loạt bằng cách tải lên file dữ liệu mới.

---

## 📁 Định Dạng Cấu Trúc File Dữ Liệu Đầu Vào

Tệp tin nạp vào hệ thống để ứng dụng phân tích chính xác cần tuân thủ cấu trúc Schema dưới đây:
* **Định dạng cho phép:** `.csv`, `.xlsx`, hoặc `.xls`.
* **Tập hợp các trường đầu vào biến độc lập (X):** Bao gồm chuẩn xác 14 cột định lượng mang tên tương ứng từ `X_1`, `X_2`, `X_3`, ..., cho đến `X_14`.
* **Cột biến nhãn mục tiêu phân loại (y):** Phải chứa cột mang tên `default` nhận hai giá trị nhị phân chính: `0` (Giao dịch an toàn / bình thường) và `1` (Giao dịch có chỉ dấu gian lận / rủi ro).

---

## 🛠️ Hướng Dẫn Cài Đặt Môi Trường & Khởi Chạy

### 1. Khởi tạo môi trường ảo độc lập
Khuyến nghị sử dụng phiên bản Python từ **3.9 đến 3.12**. Khởi tạo môi trường độc lập nhằm tránh các xung đột thư viện cục bộ:
```bash
# Khởi tạo môi trường ảo
python -m venv venv

# Kích hoạt trên môi trường Windows
venv\Scripts\activate

# Kích hoạt trên môi trường macOS / Linux
source venv/bin/activate
2. Cài đặt toàn bộ các thư viện phụ thuộc
Thực hiện cài đặt tự động các gói thư viện đã chỉ định bằng tập lệnh:

Bash
pip install -r requirements.txt
3. Khởi chạy máy chủ Web Streamlit
Chạy câu lệnh dưới đây để kích hoạt ứng dụng trên máy chủ cục bộ:

Bash
streamlit run app.py
Sau khi hệ thống khởi động hoàn tất, giao diện ứng dụng sẽ tự động hiển thị trên trình duyệt web mặc định tại địa chỉ: http://localhost:8501.

hãy chỉnh lại và xuất file app.py để in đậm và tô màu xanh dương các dữ liệu trong hình trên. giữ nguyên các đoạn mã còn lại

Tôi đã tiến hành cập nhật lại mã nguồn app.py dựa trên bức hình giao diện bạn yêu cầu. Các thông tin động hiển thị trạng thái hệ thống như: tên tệp tin kết nối, số dòng, số cột, tên thuật toán đang chạy kiểm định, cũng như số lượng dòng kết quả quét rủi ro đã được định dạng in đậm và tô màu xanh dương bằng cú pháp markdown :blue[...] chuẩn của Streamlit.

Hệ thống mã nguồn xử lý đa thuật toán (Random Forest, Decision Tree, Logistic Regression) và các logic phân chia dữ liệu, giữ tabs vẫn được bảo toàn nguyên vẹn.

Your PDF, CSV, XLSX file is ready
PY icon
 app 
 PY 

Các vị trí đoạn mã đã được chỉnh sửa để định dạng màu sắc:
Thông tin tệp nạp vào hệ thống:

Python
# Cũ: st.caption(f"📁 Đang kết nối tệp: **{uploaded_file.name}** | Kích thước: **{df.shape[0]} dòng** × **{df.shape[1]} cột**.")
st.markdown(f"📁 Đang kết nối tệp: **:blue[{uploaded_file.name}]** | Kích thước: **:blue[{df.shape[0]:,}] dòng** × **:blue[{df.shape[1]}] cột**.")
Tiêu đề tên thuật toán tại Tab 3 (Kiểm định):

Python
# Cũ: st.subheader(f"🔬 Kết Quả Kiểm Định Thuật Toán: {current_model_type}")
st.subheader(f"🔬 Kết Quả Kiểm Định Thuật Toán: **:blue[{current_model_type}]**")
Thông báo kết quả quét dữ liệu hàng loạt tại Tab 4:

Python
# Cũ: st.success(f"Xử lý hoàn tất! Đã chấm điểm rủi ro tự động cho {df_bulk.shape[0]} giao dịch thành công.")
st.success(f"Xử lý hoàn tất! Đã chấm điểm rủi ro tự động cho **:blue[{df_bulk.shape[0]}]** giao dịch thành công.")

# Cũ: st.warning(f"🚨 Phát hiện chỉ dấu rủi ro tại **{total_alerts}** dòng hồ sơ giao dịch bất thường.")
st.warning(f"🚨 Phát hiện chỉ dấu rủi ro tại **:blue[{total_alerts}]** dòng hồ sơ giao dịch bất thường.")



Gemini is AI and can make mistakes.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import io

# 1) CONFIGURATION LÀ LỆNH STREAMLIT ĐẦU TIÊN
st.set_page_config(
    layout="wide",
    page_title="Hệ Thống Chẩn Đoán Giao Dịch Rủi Ro",
    page_icon="🛡️"
)

# 2) HÀM NẠP DỮ LIỆU DÙNG CHUNG CÓ CACHE
@st.cache_data
def load_data(file_bytes, file_name):
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file dữ liệu: {e}")
        return None

# Định nghĩa tập biến đầu vào X và biến mục tiêu y từ thiết kế hệ thống
MODEL_FEATURES = [f"X_{i}" for i in range(1, 15)]
TARGET_COL = "default"

# 3) SIDEBAR - VÙNG CẤU HÌNH DỮ LIỆU & THAM SỐ ĐỘNG
with st.sidebar:
    st.header("⚙️ Cấu hình & Tải dữ liệu")
    
    # Nạp file mẫu
    uploaded_file = st.file_uploader(
        "Tải lên tệp dữ liệu mẫu", 
        type=["csv", "xlsx"],
        help="Hỗ trợ định dạng CSV hoặc Excel chứa các cột X_1 đến X_14 và cột mục tiêu default"
    )
    
    st.divider()
    st.subheader("🤖 Lựa chọn Mô hình")
    
    # Hộp chọn thuật toán huấn luyện
    model_choice = st.selectbox(
        "Thuật toán huấn luyện:",
        options=["Random Forest", "Decision Tree", "Logistic Regression"],
        index=0,
        help="Chọn thuật toán học máy phù hợp để phân tích và phân loại rủi ro giao dịch."
    )
    
    st.divider()
    st.subheader("🎛️ Tham số mô hình AI")
    
    # Thiết lập giao diện tham số động (Dynamic UI) dựa trên mô hình được chọn
    params = {}
    
    if model_choice == "Random Forest":
        params['n_estimators'] = st.slider(
            "Số lượng cây (n_estimators)", 
            min_value=10, max_value=500, value=100, step=10,
            help="Số lượng cây quyết định phối hợp ngẫu nhiên trong rừng."
        )
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['criterion'] = st.selectbox("Tiêu chí phân tách (criterion)", ["gini", "entropy", "log_loss"], index=0)
            params['max_depth'] = st.slider("Độ sâu tối đa (max_depth)", 2, 50, 15)
            params['min_samples_split'] = st.slider("Mẫu tối thiểu để tách nút", 2, 20, 2)
            
    elif model_choice == "Decision Tree":
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['criterion'] = st.selectbox("Tiêu chí phân tách (criterion)", ["gini", "entropy", "log_loss"], index=0)
            params['max_depth'] = st.slider("Độ sâu tối đa (max_depth)", 2, 50, 10)
            params['min_samples_split'] = st.slider("Mẫu tối thiểu để tách nút", 2, 20, 2)
            
    elif model_choice == "Logistic Regression":
        params['max_iter'] = st.slider(
            "Số vòng lặp tối đa (max_iter)",
            min_value=100, max_value=2000, value=1000, step=100,
            help="Số lượng vòng lặp tối đa cho các thuật toán tối ưu hội tụ."
        )
        params['C'] = st.number_input(
            "Hệ số nghịch đảo chính quy hóa (C)",
            min_value=0.001, max_value=100.0, value=1.0, step=0.1, format="%.3f",
            help="Giá trị C càng nhỏ thì mức độ chính quy hóa (regularization) càng mạnh nhằm giảm quá khớp."
        )
        params['random_state'] = st.number_input(
            "Trạng thái ngẫu nhiên (random_state)",
            min_value=0, max_value=9999, value=42, step=1
        )
        with st.expander("🛠️ Cấu hình nâng cao"):
            params['penalty'] = st.selectbox("Phương thức phạt (penalty)", ["l2", None], index=0)
            params['solver'] = st.selectbox("Thuật toán tối ưu (solver)", ["lbfgs", "newton-cg", "saga"], index=0)

    st.divider()
    
    # Nút thực hiện tác vụ huấn luyện duy nhất đặt ở dưới cùng
    train_clicked = st.button(
        "🚀 Huấn Luyện Mô Hình", 
        type="primary", 
        use_container_width=True,
        help="Nhấp để chia dữ liệu Train/Test và huấn luyện thuật toán đang được lựa chọn."
    )

# 4) HEADER - VÙNG ĐỊNH HƯỚNG TRẠNG THÁI
st.title("🛡️ Ứng Dụng Phát Hiện Giao Dịch Gian Lận & Rủi Ro")
st.caption("Giao diện phân tích đa mô hình học máy: Hỗ trợ đánh giá, so sánh hiệu năng thuật toán và chấm điểm hồ sơ tài chính.")

if uploaded_file is None:
    st.info("💡 Hệ thống đang trống dữ liệu. Vui lòng tải file mẫu (.csv / .xlsx) tại Sidebar bên trái để tiếp tục.")
    st.stop()

# Đọc dữ liệu thô thông qua hàm cache
file_bytes = uploaded_file.read()
df = load_data(file_bytes, uploaded_file.name)

if df is None:
    st.error("Lỗi: Không thể phân tích cú pháp tệp dữ liệu đã tải lên.")
    st.stop()

# ĐẶT IN ĐẬM VÀ TÔ MÀU XANH DƯƠNG CHO TÊN FILE VÀ QUY MÔ DỮ LIỆU BẰNG CẤU TRÚC MARKDOWN :blue[...] VÀ **...**
st.markdown(f"📁 Đang kết nối tệp: **:blue[{uploaded_file.name}]** | Kích thước: **:blue[{df.shape[0]:,}] dòng** × **:blue[{df.shape[1]}] cột**.")
st.divider()

# 5) KHỐI XỬ LÝ TRAIN VÀ LƯU SESSION STATE KHI BẤM NÚT
if train_clicked:
    missing_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col not in df.columns]
    if missing_cols:
        st.error(f"Dữ liệu tải lên không hợp lệ, thiếu các trường quan trọng: {missing_cols}")
    else:
        with st.spinner(f"Đang tiến hành huấn luyện thuật toán {model_choice}..."):
            X = df[MODEL_FEATURES]
            y = df[TARGET_COL]
            
            # Phân tách tập dữ liệu với tỷ lệ mẫu test 20%
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=params['random_state'])
            
            # Khởi tạo thuật toán dựa theo cấu hình động
            if model_choice == "Random Forest":
                model = RandomForestClassifier(
                    n_estimators=params['n_estimators'],
                    criterion=params['criterion'],
                    max_depth=params['max_depth'],
                    min_samples_split=params['min_samples_split'],
                    random_state=params['random_state']
                )
            elif model_choice == "Decision Tree":
                model = DecisionTreeClassifier(
                    criterion=params['criterion'],
                    max_depth=params['max_depth'],
                    min_samples_split=params['min_samples_split'],
                    random_state=params['random_state']
                )
            elif model_choice == "Logistic Regression":
                model = LogisticRegression(
                    max_iter=params['max_iter'],
                    C=params['C'],
                    penalty=params['penalty'],
                    solver=params['solver'],
                    random_state=params['random_state']
                )
                
            # Thực thi huấn luyện pipeline
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Đóng gói và lưu trữ đồng bộ vào Session State để các Tab dùng chung không bị mất dữ liệu
            st.session_state['active_model'] = model
            st.session_state['model_type'] = model_choice
            st.session_state['trained_features'] = MODEL_FEATURES
            st.session_state['metrics_results'] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'confusion': confusion_matrix(y_test, y_pred),
                'report': classification_report(y_test, y_pred, output_dict=True)
            }
            st.success(f"🎉 Đã hoàn tất huấn luyện mô hình thành công!")

# 6) PHÂN CHIA TABS HIỂN THỊ KẾT QUẢ VÀ NGHIỆP VỤ
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Phân Tích Tổng Quan", 
    "📈 Trực Quan Hóa Biến", 
    "🔬 Kiểm Định & Đánh Giá", 
    "🔮 Ứng Dụng Chẩn Đoán"
])

# --- TAB 1: PHÂN TÍCH TỔNG QUAN ---
with tab1:
    st.subheader("Đặc trưng và Thống kê Dữ liệu Huấn luyện")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng số bản ghi", f"{df.shape[0]:,}")
    col_m2.metric("Số lượng cột thuộc tính", df.shape[1])
    col_m3.metric("Dung lượng file", f"{(len(file_bytes)/(1024*1024)):.2f} MB")
    
    st.markdown("##### Bản xem trước dữ liệu mẫu (5 dòng đầu):")
    st.dataframe(df.head(5), use_container_width=True)
    
    st.markdown("##### Thống kê mô tả toán học của các biến đặc trưng:")
    active_cols = [col for col in MODEL_FEATURES + [TARGET_COL] if col in df.columns]
    st.dataframe(df[active_cols].describe(), use_container_width=True)

# --- TAB 2: TRỰC QUAN HÓA BIẾN ---
with tab2:
    st.subheader("Biểu đồ Phân Phối Tần Suất Đặc Trưng")
    
    if TARGET_COL in df.columns:
        st.markdown("##### 1. Tỷ lệ phân bổ biến mục tiêu rủi ro (`default`)")
        target_data = df[TARGET_COL].value_counts().reset_index()
        target_data.columns = [TARGET_COL, "Số lượng"]
        target_data[TARGET_COL] = target_data[TARGET_COL].astype(str).map({'0': '0 (Bình thường)', '1': '1 (Rủi ro/Gian lận)'})
        
        fig_target = px.bar(target_data, x=TARGET_COL, y="Số lượng", color=TARGET_COL,
                            color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_target, use_container_width=True)
        
    st.markdown("##### 2. Biểu đồ phân phối chi tiết các biến đầu vào X")
    valid_features = [col for col in MODEL_FEATURES if col in df.columns]
    
    selected_features = st.multiselect(
        "Tùy chọn hiển thị đồ thị (Tối đa hiển thị lưới 4 biến mặc định):",
        options=valid_features,
        default=valid_features[:4] if len(valid_features) >= 4 else valid_features
    )
    
    if selected_features:
        n_selected = len(selected_features)
        n_rows = (n_selected + 1) // 2
        for r in range(n_rows):
            grid_cols = st.columns(2)
            for c in range(2):
                f_idx = r * 2 + c
                if f_idx < n_selected:
                    feat_name = selected_features[f_idx]
                    fig_h = px.histogram(df, x=feat_name, title=f"Phân phối của {feat_name}", marginal="box")
                    fig_h.update_layout(height=350)
                    grid_cols[c].plotly_chart(fig_h, use_container_width=True)
    else:
        st.warning("Vui lòng chọn tối thiểu một trường thông tin để vẽ biểu đồ.")

# --- TAB 3: KIỂM ĐỊNH & ĐÁNH GIÁ MÔ HÌNH ---
with tab3:
    if 'active_model' not in st.session_state:
        st.info("💡 Hệ thống chưa có dữ liệu kiểm định. Vui lòng chọn tham số mô hình và nhấn nút 'Huấn Luyện Mô Hình' tại Sidebar.")
    else:
        current_model_type = st.session_state['model_type']
        metrics = st.session_state['metrics_results']
        
        # HIỂN THỊ TÊN MÔ HÌNH IN ĐẬM VÀ TÔ MÀU XANH DƯƠNG
        st.subheader(f"🔬 Kết Quả Kiểm Định Thuật Toán: **:blue[{current_model_type}]**")
        
        # Hiển thị các chỉ số cốt lõi
        c_1, c_2, c_3, c_4 = st.columns(4)
        c_1.metric("Độ chính xác (Accuracy)", f"{metrics['accuracy']:.4f}")
        c_2.metric("Độ chính xác lớp 1 (Precision)", f"{metrics['precision']:.4f}")
        c_3.metric("Độ bao phủ/Nhớ sót (Recall)", f"{metrics['recall']:.4f}")
        c_4.metric("Chỉ số cân bằng F1", f"{metrics['f1']:.4f}")
        
        st.divider()
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("##### Ma trận nhầm lẫn (Confusion Matrix)")
            cm = metrics['confusion']
            cm_dataframe = pd.DataFrame(cm, index=['Thực tế: Thường (0)', 'Thực tế: Rủi ro (1)'],
                                        columns=['Dự đoán: Thường (0)', 'Dự đoán: Rủi ro (1)'])
            st.dataframe(cm_dataframe, use_container_width=True)
            
            fig_matrix = px.imshow(cm, text_auto=True, x=['Thường (0)', 'Rủi ro (1)'], y=['Thường (0)', 'Rủi ro (1)'],
                                   color_continuous_scale='Purples', title="Heatmap Ma Trận Nhầm Lẫn")
            st.plotly_chart(fig_matrix, use_container_width=True)
            
        with col_right:
            st.markdown("##### Báo cáo phân loại chi tiết (Classification Report)")
            rep_df = pd.DataFrame(metrics['report']).transpose()
            st.dataframe(rep_df.style.format(precision=4), use_container_width=True)
            
            # Hiển thị Mức độ quan trọng hoặc Hệ số hồi quy tùy thuộc vào thuật toán
            active_model_obj = st.session_state['active_model']
            
            if hasattr(active_model_obj, 'feature_importances_'):
                st.markdown("##### Mức độ đóng góp của các biến (Feature Importance):")
                importances = active_model_obj.feature_importances_
                imp_df = pd.DataFrame({'Đặc trưng': st.session_state['trained_features'], 'Trọng số': importances}).sort_values(by='Trọng số', ascending=True)
                fig_i = px.bar(imp_df, x='Trọng số', y='Đặc trưng', orientation='h', color='Trọng số', color_continuous_scale='teal')
                fig_i.update_layout(height=350)
                st.plotly_chart(fig_i, use_container_width=True)
                
            elif hasattr(active_model_obj, 'coef_'):
                st.markdown("##### Hệ số hồi quy tuyến tính (Model Coefficients):")
                coefficients = active_model_obj.coef_[0]
                coef_df = pd.DataFrame({'Đặc trưng': st.session_state['trained_features'], 'Hệ số hồi quy': coefficients}).sort_values(by='Hệ số hồi quy')
                fig_c = px.bar(coef_df, x='Hệ số hồi quy', y='Đặc trưng', orientation='h', color='Hệ số hồi quy', color_continuous_scale='RdBu_r')
                fig_c.update_layout(height=350)
                st.plotly_chart(fig_c, use_container_width=True)

# --- TAB 4: ỨNG DỤNG CHẨN ĐOÁN DỮ LIỆU MỚI ---
with tab4:
    if 'active_model' not in st.session_state:
        st.info("💡 Vui lòng kích hoạt huấn luyện mô hình ở cấu hình trước khi sử dụng tính năng dự đoán rủi ro.")
    else:
        active_model_obj = st.session_state['active_model']
        
        mode = st.radio(
            "Chọn chế độ nạp hồ sơ giao dịch mới cần kiểm thử:",
            options=["Chẩn đoán hồ sơ đơn lẻ (Form nhập trực tiếp)", "Dự đoán hàng loạt theo danh sách (Upload File Tệp)"],
            horizontal=True
        )
        
        if mode == "Chẩn đoán hồ sơ đơn lẻ (Form nhập trực tiếp)":
            st.markdown("##### Điền các thông số kỹ thuật số đo giao dịch hiện hành:")
            
            with st.form("form_single_predict"):
                form_inputs = {}
                f_col1, f_col2 = st.columns(2)
                
                for idx, col_feat in enumerate(MODEL_FEATURES):
                    # Khởi tạo giá trị mặc định bằng trung vị mẫu huấn luyện nhằm đảm bảo logic nghiệp vụ
                    if col_feat in df.columns:
                        v_min = float(df[col_feat].min())
                        v_max = float(df[col_feat].max())
                        v_med = float(df[col_feat].median())
                    else:
                        v_min, v_max, v_med = -5.0, 5.0, 0.0
                        
                    with f_col1 if idx % 2 == 0 else f_col2:
                        form_inputs[col_feat] = st.number_input(
                            f"Giá trị thông số {col_feat}",
                            min_value=v_min*3.0, max_value=v_max*3.0, value=v_med, format="%.6f",
                            help=f"Khoảng giá trị mẫu huấn luyện: [{v_min:.2f}, {v_max:.2f}]"
                        )
                        
                btn_diagnose = st.form_submit_button("Tiến Hành Chẩn Đoán", type="primary", use_container_width=True)
                
            if btn_diagnose:
                single_payload = pd.DataFrame([form_inputs])[MODEL_FEATURES]
                pred_label = active_model_obj.predict(single_payload)[0]
                
                st.markdown("---")
                st.markdown("##### Kết luận chẩn đoán hệ thống:")
                
                res_col1, res_col2 = st.columns(2)
                if pred_label == 1:
                    res_col1.error("⚠️ CẢNH BÁO NGUY HIỂM: Giao dịch có dấu hiệu bất thường / Rủi ro cao.")
                else:
                    res_col1.success("✅ HỆ THỐNG AN TOÀN: Giao dịch có chỉ số bình thường, độ tin cậy cao.")
                    
                if hasattr(active_model_obj, "predict_proba"):
                    probs = active_model_obj.predict_proba(single_payload)[0]
                    # ĐẶT IN ĐẬM VÀ TÔ MÀU XANH DƯƠNG CHO XÁC SUẤT RỦI RO ĐƠN LẺ
                    st.markdown(f"Xác suất rủi ro phát hiện: **:blue[{probs[1]*100:.2f} %]**")
                    res_col2.progress(float(probs[1]))
                    
        elif mode == "Dự đoán hàng loạt theo danh sách (Upload File Tệp)":
            st.markdown("##### Quét kiểm tra danh sách rủi ro đồng loạt bằng Tệp tin:")
            st.caption("Yêu cầu định dạng cấu trúc tệp: Tệp tải lên phải chứa đầy đủ cấu trúc tên cột từ `X_1` tới `X_14`.")
            
            bulk_file = st.file_uploader("Nạp tệp Excel/CSV danh sách cần quét:", type=["csv", "xlsx"], key="bulk_key")
            
            if bulk_file is not None:
                bulk_bytes = bulk_file.read()
                df_bulk = load_data(bulk_bytes, bulk_file.name)
                
                if df_bulk is not None:
                    missing_bulk = [c for c in MODEL_FEATURES if c not in df_bulk.columns]
                    if missing_bulk:
                        st.error(f"Quét file thất bại! Thiếu các cột biến đầu vào sau trong cấu trúc file nạp: {missing_bulk}")
                    else:
                        bulk_payload = df_bulk[MODEL_FEATURES]
                        predictions = active_model_obj.predict(bulk_payload)
                        
                        df_output = df_bulk.copy()
                        df_output['Du_Bao_Rui_Ro'] = predictions
                        
                        if hasattr(active_model_obj, "predict_proba"):
                            df_output['Xac_Suat_Rui_Ro'] = active_model_obj.predict_proba(bulk_payload)[:, 1]
                            
                        # ĐẶT IN ĐẬM VÀ TÔ MÀU XANH DƯƠNG CHO SỐ LƯỢNG GIAO DỊCH QUÉT THÀNH CÔNG
                        st.success(f"Xử lý hoàn tất! Đã chấm điểm rủi ro tự động cho **:blue[{df_bulk.shape[0]}]** giao dịch thành công.")
                        
                        total_alerts = int(np.sum(predictions))
                        # ĐẶT IN ĐẬM VÀ TÔ MÀU XANH DƯƠNG CHO SỐ DÒNG BẤT THƯỜNG
                        st.warning(f"🚨 Phát hiện chỉ dấu rủi ro tại **:blue[{total_alerts}]** dòng hồ sơ giao dịch bất thường.")
                        
                        st.markdown("##### Bảng theo dõi kết quả quét hàng loạt:")
                        st.dataframe(df_output, use_container_width=True)
                        
                        # Xuất dữ liệu tải về dưới dạng CSV tiêu chuẩn mã hóa utf-8-sig
                        buffer_csv = io.StringIO()
                        df_output.to_csv(buffer_csv, index=False, encoding='utf-8-sig')
                        csv_payload_string = buffer_csv.getvalue()
                        
                        st.download_button(
                            label="📥 Tải Xuống Bảng Kết Quả Định Giá (.CSV)",
                            data=csv_payload_string,
                            file_name="ket_qua_quet_rui_ro_giao_dich.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
app.py
Displaying app.py.
