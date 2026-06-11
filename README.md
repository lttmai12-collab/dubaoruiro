# 🛡️ Ứng dụng Web Phát hiện Giao dịch Gian lận Tài chính

Ứng dụng web tương tác trực quan được xây dựng hoàn toàn bằng **Streamlit** và mô hình Học máy **Random Forest Classifier**. Hệ thống cho phép các chuyên viên phân tích rủi ro dễ dàng tải dữ liệu, thay đổi siêu tham số mô hình động, đánh giá chất lượng phân loại và thực hiện dự báo rủi ro gian lận cho cả các giao dịch đơn lẻ lẫn tệp dữ liệu lớn.

## ✨ Tính năng chính
- **Cấu hình & Tải dữ liệu sống:** Tải lên dữ liệu tập huấn luyện linh hoạt ở thanh Sidebar, điều chỉnh trực tiếp các tham số của thuật toán Random Forest (`n_estimators`, `max_depth`, `random_state`).
- **Tổng quan dữ liệu:** Hiển thị trực quan dữ liệu thô, các chiều kích thước, thống kê toán học mô tả của 14 biến tính năng `X_1` tới `X_14`.
- **Trực quan hóa đồ họa:** Vẽ biểu đồ tần suất phân phối lớp dữ liệu (`default`) và mật độ phân tán các biến số tự động qua thư viện Plotly sắc nét.
- **Đánh giá kiểm định mô hình:** Tái hiện chính xác các thang đo chuẩn bao gồm: Accuracy, Precision, Recall, F1-Score cùng Ma trận nhầm lẫn (Confusion Matrix) và Đồ thị đóng góp độ quan trọng của thuộc tính đầu vào (Feature Importance).
- **Dự báo linh hoạt (2 chế độ):** - Nhập thủ công các thông số giao dịch cụ thể để nhận kết quả chấm điểm rủi ro lập tức.
  - Tải lên tệp khách hàng/giao dịch mới (`X_new`) để quét và tải xuống báo cáo phân loại hàng loạt.

## 📁 Cấu trúc tệp dữ liệu đầu vào chuẩn
Tệp dữ liệu tải lên hệ thống yêu cầu định dạng `.csv` hoặc `.xlsx` tuân thủ cấu trúc:
- **Biến đặc trưng (14 cột):** `X_1`, `X_2`, `X_3`, `X_4`, `X_5`, `X_6`, `X_7`, `X_8`, `X_9`, `X_10`, `X_11`, `X_12`, `X_13`, `X_14` (Kiểu dữ liệu Số).
- **Biến mục tiêu (01 cột nhãn):** Cột mang tên `default` nhận giá trị nhị phân `0` (Giao dịch bình thường) hoặc `1` (Giao dịch gian lận/Rủi ro).

---

## 🛠️ Hướng dẫn Cài đặt & Khởi chạy ứng dụng

### Bước 1: Chuẩn bị môi trường máy tính
Đảm bảo máy tính của bạn đã cài đặt sẵn môi trường **Python 3.9** trở lên.

### Bước 2: Cài đặt các thư viện phụ thuộc bắt buộc
Mở terminal/command prompt tại thư mục chứa mã nguồn ứng dụng và chạy lệnh:
```bash
pip install -r requirements.txt
