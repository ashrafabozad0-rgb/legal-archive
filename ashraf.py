import streamlit as st
from datetime import date

# إعدادات الواجهة
st.set_page_config(page_title="الإدارة القانونية - أشرف الحويج", page_icon="⚖️", layout="wide")

# الترويسة مع أيقونة واتساب بجانب الرقم
st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <div style="text-align: center; background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-bottom: 5px solid #1E3A8A; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
        <h1 style="color: #1E3A8A; margin: 0;">الإدارة القانونية لشركة إيجيبت ساينتيفك</h1>
        <h2 style="color: #4B5563; margin: 10px 0;">إعداد المستشار/ أشرف الحويج المحامي</h2>
        <p style="font-size: 20px; color: #1E3A8A; font-weight: bold;">
             واتساب وموبايل: <a href="https://wa.me/201145134595" style="text-decoration: none; color: #25D366;">
             <i class="fab fa-whatsapp"></i> 01145134595</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# إدارة حالة الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None

# --- صفحة الدخول والتسجيل ---
if not st.session_state['logged_in']:
    tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 طلب حساب جديد (للموظفين)"])
    
    with tab_login:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            login_role = st.selectbox("الدخول بصفتك:", ["الأدمن (المستشار أشرف)", "موظف / مستخدم"], key="role_sel")
            u_name = st.text_input("اسم المستخدم", key="u_name")
            u_pass = st.text_input("كلمة المرور", type="password", key="u_pass")
            
            if st.button("دخول النظام", use_container_width=True):
                if login_role == "الأدمن (المستشار أشرف)" and u_name == "ASHRAF2026" and u_pass == "Ashraf@2026":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "admin"
                    st.rerun()
                elif login_role == "موظف / مستخدم" and u_name == "user" and u_pass == "1234":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "user"
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        st.info("قم بتعبئة البيانات التالية لطلب صلاحية الدخول للأرشيف")
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("الاسم ثلاثي")
            st.text_input("الرقم القومي")
            st.date_input("تاريخ الميلاد", min_value=date(1960,1,1))
        with col_b:
            st.text_input("رقم الموبايل")
            st.selectbox("الصفة الوظيفية", ["محاسب", "مهندس", "محامي", "رئيس مجلس الإدارة", "عضو مجلس إدارة"])
            st.file_uploader("رفع صورة البطاقة الشخصية (وجهين)")
        
        if st.button("إرسال طلب التسجيل للأدمن"):
            st.success("تم إرسال طلبك بنجاح للمستشار أشرف. سيتم إخطارك عند التفعيل.")

# --- الصفحة الرئيسية (بعد الدخول) ---
else:
    role = st.session_state['role']
    st.sidebar.title(f"مرحباً: {'سيادة المستشار' if role == 'admin' else 'أستاذ موظف'}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

    if role == "admin":
        st.title("🛠️ لوحة تحكم الأدمن (صلاحيات كاملة)")
        # هنا الأدمن يقدر يرفع ويعدل
        st.file_uploader("ارفع ملفات الشركة الجديدة")
        st.button("تحديث وتنسيق الأرشيف")
    else:
        st.title("📑 أرشيف الموظفين (للاطلاع فقط)")
        st.text_input("🔍 ابحث عن عقد أو مستند بالاسم...")
        st.write("قائمة الملفات التي وافق الأدمن على عرضها ستظهر هنا.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>جميع الحقوق محفوظة © المستشار أشرف الحويج 2026</p>", unsafe_allow_html=True)