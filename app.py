import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 본인의 API 키를 여기에 입력 (따옴표 유지)
MY_API_KEY = "AIzaSyAklVNMIukXpHHmhh95xdBta8oPdOfYtrc"

# 2. 앱 기본 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="🎓")

# 스타일 패치 (최신 브라우저 호환)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 문제집 텍스트 복원기")
st.write("공유 금지 혼자쓰셈")

# 3. 사진 업로드
uploaded_file = st.file_uploader("문제집 사진 선택", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # 로그 피드백 반영: width='stretch' 사용
    st.image(image, caption="업로드된 이미지", width='stretch')

    if st.button("✨ 텍스트 추출 시작"):
        if MY_API_KEY == "여기에_실제_API_키를_넣으세요":
            st.error("잠깐! 질문자님, 코드 안에 API 키를 실제 키로 바꿔주셔야 해요!")
        else:
            with st.spinner("AI가 손글씨를 지우고 문제를 복원하는 중입니다..."):
                try:
                    # 최신 API 설정
                    genai.configure(api_key=MY_API_KEY)
                    
                    # 2026년 표준 모델 호출
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

                    prompt = """
                    이 이미지에서 사람이 직접 쓴 모든 글씨와 채점 흔적을 제거해줘.
                    원래 인쇄되어 있던 '문제 번호', '지문', '문제 내용', '보기'만 추출해서 
                    줄바꿈을 깔끔하게 해서 텍스트로 보여줘.
                    """
                    
                    # 이미지 분석 및 응답 생성
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        st.success("✅ 추출 성공!")
                        st.text_area("결과를 복사하세요:", value=response.text, height=500)
                    else:
                        st.warning("텍스트 인식을 못 했어. 사진을 좀 더 선명하게 찍어줄래?")
                        
                except Exception as e:
                    # 진짜 에러 원인을 화면에 아주 작게 표시 (질문자님 확인용)
                    st.error(f"연결 상태가 불안정해. (상세: {str(e)})")
                    st.info("AI Studio에서 API 키가 활성화 상태인지 확인해봐!")
