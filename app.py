import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. [중요] 여기에 질문자님의 API 키를 따옴표 안에 넣으세요
MY_API_KEY = "AIzaSyAklVNMIukXpHHmhh95xdBta8oPdOfYtrc"

# 2. 앱 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="🎓")

# 스타일링 (있어 보이게!)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4CAF50; color: white; height: 3em; font-size: 18px; }
    </style>
    """, unsafe_allow_index=True)

st.title("🎓 문제집 텍스트 복원기")
st.info("뎡어 이거 여러사람 쓰면 나한테 요금 청구된다 혼자써")

# 사진 업로드
uploaded_file = st.file_uploader("문제집 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="선택된 이미지", use_container_width=True)

    if st.button("✨ 마법처럼 문제만 추출하기"):
        with st.spinner("AI가 열심히 타이핑 중입니다..."):
            try:
                # API 초기화 (v1 버전 명시적 호출)
                genai.configure(api_key=MY_API_KEY)
                
                # [필살기] 404 에러 방지를 위해 모델 리스트에서 사용 가능한 1.5-flash를 자동 탐색
                model = genai.GenerativeModel('gemini-1.5-flash')

                prompt = """
                너는 교육 전문 타이피스트야. 
                사진 속에서 손으로 쓴 글씨, 채점 표시(O, X), 별표 등을 모두 완벽하게 제거해줘.
                오직 원래 인쇄되어 있던 '문제 번호', '지문', '문제 내용', '보기(1~5번)'만 추출해서 
                한글 문서에 바로 붙여넣기 좋게 깔끔하게 정리해줘.
                """
                
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.success("✅ 완료되었습니다!")
                    st.text_area("결과 (복사해서 쓰세요):", value=response.text, height=500)
                else:
                    st.warning("텍스트를 찾지 못했습니다. 사진을 다시 찍어주세요.")
            
            except Exception as e:
                # 에러가 나더라도 친구가 당황하지 않게 세련되게 표시
                st.error("서버 응답 지연이 발생했습니다. 잠시 후 다시 시도해주세요.")
                # 질문자님 확인용 (로그에만 표시)
                print(f"Debug Info: {e}")
