import streamlit as st
from google import genai
from PIL import Image

# 1. 본인의 API 키 입력
MY_API_KEY = "AIzaSyAklVNMIukXpHHmhh95xdBta8oPdOfYtrc"

# 2. 앱 설정
st.set_page_config(page_title="문제집 텍스트 추출기", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 문제집 텍스트 추출기")
st.write("이거 수백장 넘어가면 나한테 요금 청구됨... 혼자써야해")

# 3. 사진 업로드
uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # 최신 스트림릿 규격: use_container_width=True 대신 width='stretch' 사용
    st.image(image, caption="선택된 이미지", width='stretch')

    if st.button("✨ 텍스트 추출 시작"):
        with st.spinner("최신 AI 엔진이 분석 중입니다..."):
            try:
                # 2026년형 신규 SDK 호출 방식
                client = genai.Client(api_key=MY_API_KEY)
                
                prompt = """
                이미지 속 손글씨와 채점 흔적을 모두 지우고, 
                원래 인쇄된 문제와 보기만 아주 깔끔하게 텍스트로 추출해줘. 
                한글 문서(HWP) 편집이 편하게 문제 번호 순서대로 정리해줘.
                """
                
                # 신규 모델 호출 (gemini-2.0-flash 혹은 1.5-flash)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt, image]
                )
                
                if response.text:
                    st.success("✅ 추출 성공!")
                    st.text_area("결과 (복사해서 쓰세요):", value=response.text, height=500)
                else:
                    st.warning("내용을 읽지 못했어. 사진을 다시 찍어볼래?")
            
            except Exception as e:
                st.error("연결 오류가 발생했어. 잠시 후 다시 시도해줘!")
                # 로그 확인용
                print(f"Update Required: {e}")
