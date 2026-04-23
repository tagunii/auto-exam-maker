import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 본인의 API 키를 여기에 입력 (따옴표 유지)
MY_API_KEY = "AIzaSyCsSeQbMWsp8a-WMKAZGNT62he5sILf3bE"

# 2. 앱 기본 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 문제집 텍스트 복원기")
st.write("공유 금지 혼자쓰시길")

# 3. 사진 업로드
uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", width='stretch')

    if st.button("✨ 텍스트 추출 시작"):
        if MY_API_KEY == "여기에_실제_API_키를_넣으세요":
            st.error("코드 내의 API 키를 실제 키로 수정해주세요!")
        else:
            with st.spinner("AI가 분석 중입니다..."):
                try:
                    # [수정] 들여쓰기를 정확히 맞추고 REST 방식으로 접속 시도
                    genai.configure(api_key=MY_API_KEY, transport='rest')
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    prompt = "이미지에서 손글씨와 채점 흔적을 제외하고 인쇄된 문제 텍스트만 추출해줘."
                    
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        st.success("✅ 추출 성공!")
                        st.text_area("결과 복사:", value=response.text, height=500)
                    else:
                        st.warning("텍스트를 인식하지 못했어.")
                        
                except Exception as e:
                    # 상세 에러가 v1beta 404라면 모델 이름을 'models/gemini-1.5-flash'로 바꿔야 할 수도 있음
                    st.error(f"오류가 발생했습니다: {str(e)}")
