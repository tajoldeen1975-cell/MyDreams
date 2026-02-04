
import streamlit as st
import g4f
import nest_asyncio
import asyncio

# إعدادات الصفحة (يجب أن تكون أول سطر في الكود)
st.set_page_config(
    page_title="مفسر الأحلام الشامل",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تطبيق إصلاح مشاكل التزامن
nest_asyncio.apply()

# --- تنسيق CSS لدعم اللغة العربية والاتجاه من اليمين لليسار ---
st.markdown("""
<style>
    /* تعيين الخط والاتجاه العام */
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق العناوين */
    h1 {
        color: #1abc9c;
        text-align: center;
        font-family: 'Amiri', serif;
    }
    
    /* تنسيق حقول الإدخال */
    .stTextArea textarea {
        direction: rtl;
        text-align: right;
        font-size: 18px !important;
        border: 2px solid #1abc9c;
    }
    
    /* تنسيق الأزرار */
    .stButton button {
        width: 100%;
        background-color: #1abc9c;
        color: white;
        font-size: 20px;
        border-radius: 10px;
    }
    .stButton button:hover {
        background-color: #16a085;
        color: white;
    }
    
    /* تنسيق رسائل التنبيه */
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء القائمة العلوية الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- دالة التفسير ---
async def get_interpretation(scholar, text):
    base_instruction = "أنت خبير تفسير أحلام، لغتك عربية فصحى رصينة، تبدأ ببسم الله وتختم بـ 'والله تعالى أعلم'."
    
    if scholar == "الإمام الصادق (ع)":
        specific = "تعتمد حصراً على تراث الإمام جعفر الصادق (عليه السلام). ركز على 'الوجوه' والروايات المعتبرة."
    elif scholar == "ابن سيرين":
        specific = "تعتمد حصراً على منهج ابن سيرين (القياس والدلالات القرآنية)."
    elif scholar == "النابلسي":
        specific = "تعتمد حصراً على منهج النابلسي (الحالة الاجتماعية والرموز الدقيقة)."
    elif scholar == "ابن شاهين":
        specific = "تعتمد حصراً على منهج ابن شاهين (تصنيف الرؤيا حسب نوع الرائي)."
    else:
        specific = "أنت 'المفسر الجامع'. قارن بين المدارس وأعطِ الخلاصة الجامعة."

    prompt = f"{base_instruction}\n{specific}\nالحلم: '{text}'\nالمطلوب: تفسير دقيق وشامل."

    try:
        # استخدام g4f للاتصال بالذكاء الاصطناعي
        response = await asyncio.to_thread(
            g4f.ChatCompletion.create,
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    except Exception as e:
        return f"⚠️ عذراً، حدث خطأ في الاتصال: {str(e)}\nيرجى المحاولة مرة أخرى."

# --- واجهة التطبيق ---
st.title("🕌 موسوعة تفسير الأحلام الكبرى")
st.markdown("<h5 style='text-align: center; color: gray;'>تفسير دقيق بالذكاء الاصطناعي استناداً لأمهات الكتب</h5>", unsafe_allow_html=True)
st.divider()

# المدخلات
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📜 اختر المنهج")
    scholar_choice = st.radio(
        "المفسر:",
        ["التفسير الشامل (الأمثل)", "الإمام الصادق (ع)", "ابن سيرين", "النابلسي", "ابن شاهين"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 💤 تفاصيل الرؤيا")
    dream_text = st.text_area("اكتب حلمك هنا...", height=150, placeholder="رأيت في المنام أنني...")

# زر البحث
if st.button("تفسير الرؤيا ✨"):
    if not dream_text.strip():
        st.warning("يرجى كتابة تفاصيل الحلم أولاً.")
    else:
        with st.spinner('جاري استشارة المفسر الآلي... يرجى الانتظار'):
            # تشغيل الدالة
            result = asyncio.run(get_interpretation(scholar_choice, dream_text))
            
            # عرض النتيجة
            st.success("تم التفسير بنجاح!")
            st.markdown("---")
            st.markdown(f"""
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-right: 5px solid #1abc9c;">
                {result}
            </div>
            """, unsafe_allow_html=True)
