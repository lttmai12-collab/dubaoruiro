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
