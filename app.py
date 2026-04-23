import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. [필수] 여기에 본인의 API 키를 입력하세요
MY_API_KEY = "AIzaSyAklVNMIukXpHHmhh95xdBta8oPdOfYtrc"

# 2. 앱 기본 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="🎓")

# 3. 화면 스타일 적용 (오류 수정됨)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 문제집 텍스트 복원기")
st.write("이거 여러사람 쓰면 나한테 요금 청구돼.. 혼자 써")

# 4. 사진 업로드 및 처리
uploaded_file = st.file_uploader("문제집 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="선택된 이미지", use_container_width=True)

    if st.button("✨ 텍스트 추출 시작"):
        with st.spinner("AI가 분석 중입니다... 잠시만 기다려줘!"):
            try:
                # API 연결
                genai.configure(api_key=MY_API_KEY)
                
                # 모델 설정 (가장 안정적인 호출 방식)
                model = genai.GenerativeModel('gemini-1.5-flash')

                prompt = """
                사진 속에서 손으로 쓴 풀이, 정답 체크, 메모 등을 모두 무시하고, 
                원래 인쇄되어 있던 '문제'와 '보기'만 정확히 텍스트로 추출해줘.
                한글 문서(HWP)에 바로 붙여넣기 좋게 깔끔하게 정리해줘.
                """
                
                # 결과 생성
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("✅ 추출 성공!")
                    st.text_area("결과 (그대로 복사해서 쓰면 돼):", value=response.text, height=500)
                else:
                    st.warning("텍스트를 인식하지 못했어. 조금 더 밝은 곳에서 다시 찍어볼래?")
            
            except Exception as e:
                st.error("앗, 구글 서버랑 연결이 잠시 끊겼어. 다시 한번 눌러봐!")
                # 로그 확인용 (사용자에겐 보이지 않음)
                print(f"Error details: {e}")
