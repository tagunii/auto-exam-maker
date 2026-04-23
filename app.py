import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 (꼭 새로 만든 키인지 확인해주세요!)
MY_API_KEY = "AIzaSyDXfEJYt0w0xVjRBNuhlQHGIkLuYjM8uLk"

st.set_page_config(page_title="문제집 텍스트 복원기")
st.title("🎓 문제집 텍스트 복원기")

uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드됨", width=500)

    if st.button("✨ 텍스트 추출 시작"):
        with st.spinner("분석 중..."):
            try:
                genai.configure(api_key=MY_API_KEY)
                
                # [해결책] 1.5-flash 대신, 가장 호환성이 높은 모델명으로 변경
                # 만약 이것도 안 되면 'gemini-1.0-pro-vision-latest'로 시도하세요.
                model = genai.GenerativeModel('gemini-pro-vision')

                response = model.generate_content(["이미지에서 손글씨를 제외한 문제만 추출해줘.", image])
                
                if response.text:
                    st.success("✅ 완료!")
                    st.text_area("결과:", value=response.text, height=500)
            except Exception as e:
                # 에러가 나면 어떤 모델을 써야 하는지 목록을 그냥 화면에 띄워버립시다.
                st.error(f"오류 내용: {e}")
                st.write("사용 가능한 모델 목록을 확인하는 중...")
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write(available_models)
