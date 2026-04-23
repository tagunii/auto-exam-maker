import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 입력
MY_API_KEY = "AIzaSyDXfEJYt0w0xVjRBNuhlQHGIkLuYjM8uLk"

# 2. 앱 설정
st.set_page_config(page_title="문제집 텍스트 복원기")

st.title("🎓 문제집 텍스트 복원기")

uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드됨", width=500) # 규격 에러 방지를 위해 고정 수치 사용

    if st.button("✨ 텍스트 추출 시작"):
        if not MY_API_KEY or "여기에" in MY_API_KEY:
            st.error("API 키를 정확히 입력해주세요.")
        else:
            with st.spinner("AI 분석 중..."):
                try:
                    # 가장 기본적인 초기화 방식
                    genai.configure(api_key=MY_API_KEY)
                    
                    # 모델 이름을 명시적으로 지정
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    # 분석 실행
                    response = model.generate_content(["다음 이미지에서 손글씨를 제외한 문제 텍스트만 추출해줘.", image])
                    
                    if response.text:
                        st.success("✅ 완료!")
                        st.text_area("결과:", value=response.text, height=500)
                except Exception as e:
                    # 모든 복잡한 메시지를 치우고 실제 에러 내용만 간결하게 표시
                    st.error(f"오류 발생: {e}")
