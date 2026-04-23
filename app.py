import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 사용 중인 API 키
MY_API_KEY = "AIzaSyDXfEJYt0w0xVjRBNuhlQHGIkLuYjM8uLk"

st.set_page_config(page_title="문제집 텍스트 복원기")
st.title("🎓 문제집 텍스트 복원기")

uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드됨", width=500)

    if st.button("✨ 텍스트 추출 시작"):
        with st.spinner("최신 Gemini 2.5 엔진 분석 중..."):
            try:
                genai.configure(api_key=MY_API_KEY)
                
                # 리스트 0번에 있던 최신 모델명을 정확히 입력합니다.
                model = genai.GenerativeModel('gemini-2.5-flash')

                prompt = "이미지에서 손글씨와 채점 흔적을 제외하고 인쇄된 문제 텍스트만 추출해줘."
                
                # 최신 엔진은 멀티모달 성능이 압도적이라 아주 잘 읽을 겁니다.
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("✅ 추출 성공!")
                    st.text_area("결과:", value=response.text, height=500)
            except Exception as e:
                st.error(f"오류 발생: {e}")
