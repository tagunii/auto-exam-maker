import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 새로 발급받은 API 키를 여기에 넣으세요
MY_API_KEY = "AIzaSyDXfEJYt0w0xVjRBNuhlQHGIkLuYjM8uLk"

# 2. 앱 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="🎓")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 문제집 텍스트 복원기")

uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드됨", width='stretch')

    if st.button("✨ 텍스트 추출 시작"):
        with st.spinner("AI가 분석 중입니다..."):
            try:
                # [필살기] v1 정식 버전 통로를 강제로 사용하도록 설정
                # 이 설정이 v1beta 404 에러를 원천 봉쇄합니다.
                genai.configure(api_key=MY_API_KEY, transport='rest', client_options={'api_version': 'v1'})
                
                # 모델 이름 앞에 models/ 를 붙여 경로를 명확히 합니다.
                model = genai.GenerativeModel('models/gemini-1.5-flash')

                prompt = "이미지에서 손글씨와 채점 흔적을 제외하고 인쇄된 문제 텍스트만 추출해줘."
                
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("✅ 추출 성공!")
                    st.text_area("결과 복사:", value=response.text, height=500)
                else:
                    st.warning("텍스트를 인식하지 못했어.")
                        
            except Exception as e:
                st.error(f"시스템 연결 오류: {str(e)}")
