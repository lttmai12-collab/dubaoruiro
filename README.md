# 🛡️ Ứng dụng phát hiện giao dịch gian lận (Streamlit Web App)

Dự án này chuyển đổi mô hình phân loại học máy (`RandomForestClassifier`) từ môi trường thử nghiệm Notebook (`.ipynb`) sang một ứng dụng giao diện web trực quan tương tác thời gian thực bằng thư viện **Streamlit**.

## ✨ Tính năng chính của ứng dụng
Ứng dụng được chia bố cục khoa học theo nguyên tắc phân vùng cấu hình bền vững nằm ở thanh Sidebar và nội dung động được phân tách qua 4 Tab chính:
1. **📊 Tổng quan dữ liệu:** Hiển thị tóm tắt, kích thước tập tin, dữ liệu thô và thống kê mô tả từng đặc trưng của hệ thống (`X_1` -> `X_14`).
2. **📈 Trực quan hóa dữ liệu:** Sử dụng thư viện đồ họa động `Plotly` vẽ phân lớp mục tiêu biến `default` và phân phối mật độ phân tán các biến.
3. **🎯 Kết quả & Kiểm định:** Báo cáo chi tiết độ chính xác toàn diện bao gồm: *Accuracy, Precision, Recall, F1-Score*, đi kèm hiển thị trực quan Ma trận nhầm lẫn (Confusion Matrix).
4. **🔮 Sử dụng mô hình (Suy luận):**
   * **Nhập thông số trực tiếp:** Cho phép chuyên viên điền thông số nhanh một giao dịch bất kỳ để hệ thống đánh giá tức thì rủi ro.
   * **Tải file dữ liệu hàng loạt:** Nạp tệp dữ liệu test mới, dự đoán hàng loạt và tải tập tin kết quả trích xuất `.csv` tiện lợi.

## 📁 Cấu trúc dữ liệu đầu vào chuẩn hóa
Để ứng dụng vận hành chính xác và tránh xung đột hệ thống, tệp dữ liệu huấn luyện tải lên bắt buộc phải chứa các cấu trúc cột sau:
* **Các cột thuộc tính độc lập (14 cột):** `X_1, X_2, X_3, X_4, X_5, X_6, X_7, X_8, X_9, X_10, X_11, X_12, X_13, X_14` (Định dạng số thực/số nguyên).
* **Cột nhãn mục tiêu phụ thuộc:** `default` (Nhận giá trị phân lớp nhị phân `0` đại diện cho Giao dịch hợp lệ và `1` đại diện cho Giao dịch gian lận).

## 🚀 Hướng dẫn cài đặt và khởi chạy ứng dụng

### Bước 1: Khởi tạo môi trường ảo và cài đặt thư viện phụ thuộc
Đảm bảo bạn đã cài đặt Python (Khuyến nghị phiên bản `>=3.9` đến `3.12`). Chạy lệnh sau tại thư mục chứa mã nguồn:

```bash
pip install -r requirements.txt
