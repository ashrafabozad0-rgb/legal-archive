import streamlit as st
import pandas as pd
import os # مكتبة للتعامل مع مسارات الملفات

st.set_page_config(page_title="بوابة مستندات الشركة", layout="wide")

# 1. قاموس ربط الملفات (هنا بنربط الاسم اللي بيظهر للموظف بمكان الملف الفعلي)
file_paths = {
    "لائحة العمل": "documents/hr_rules.pdf",
    "نموذج إجازة": "documents/vacation.pdf",
    "عقد تسويق": "documents/marketing.pdf",
    "توكيل عام": "documents/power_of_attorney.pdf"
}

if 'requests' not in st.session_state:
    st.session_state.requests = pd.DataFrame(columns=["Employee", "Document", "Status"])

user_type = st.sidebar.selectbox("تسجيل الدخول كـ:", ["اختر...", "موظف", "مدير النظام"])

if user_type == "موظف":
    st.title("بوابة طلب المستندات")
    emp_name = st.text_input("اسم الموظف:")
    
    # نجيب أسماء الأوراق من القاموس اللي عملناه فوق
    docs_available = list(file_paths.keys())
    selected_doc = st.selectbox("اختر الورقة المطلوبة:", docs_available)
    
    if st.button("طلب تحميل"):
        if emp_name:
            new_req = {"Employee": emp_name, "Document": selected_doc, "Status": "Pending"}
            st.session_state.requests = pd.concat([st.session_state.requests, pd.DataFrame([new_req])], ignore_index=True)
            st.success("تم إرسال الطلب.. يرجى الانتظار لحين موافقة الإدارة.")
            
    if emp_name:
        st.subheader("حالة طلباتي:")
        my_requests = st.session_state.requests[st.session_state.requests["Employee"] == emp_name]
        
        for index, row in my_requests.iterrows():
            if row["Status"] == "Approved":
                st.write(f"✅ تمت الموافقة على: {row['Document']}")
                
                # 2. هنا خطوة الربط والتحميل الفعلي للملف
                doc_path = file_paths[row['Document']] # تحديد مسار الملف
                
                # التأكد إن الملف موجود فعلاً في الفولدر عشان ميحصلش خطأ
                if os.path.exists(doc_path):
                    with open(doc_path, "rb") as file:
                        st.download_button(
                            label="اضغط هنا لتحميل الملف", 
                            data=file, 
                            file_name=f"{row['Document']}.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error("الملف غير متوفر حالياً على السيرفر، تواصل مع الإدارة.")
            else:
                st.write(f"⏳ قيد الانتظار: {row['Document']}")

elif user_type == "مدير النظام":
    st.title("لوحة تحكم الإدارة")
    pending_reqs = st.session_state.requests[st.session_state.requests["Status"] == "Pending"]
    
    if pending_reqs.empty:
        st.info("لا توجد طلبات معلقة.")
    else:
        for index, row in pending_reqs.iterrows():
            col1, col2, col3 = st.columns(3)
            col1.write(f"الموظف: {row['Employee']}")
            col2.write(f"الورقة: {row['Document']}")
            if col3.button("موافقة", key=f"approve_{index}"):
                st.session_state.requests.at[index, "Status"] = "Approved"
                st.rerun()
