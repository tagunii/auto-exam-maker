import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 앱 기본 설정
st.set_page_config(page_title="선생님을 위한 AI 문제 추출기", page_icon="📝")

# 2. 사이드바 - 설정 영역
with st.sidebar:
    st.header("⚙️ 환경 설정")
    st.write("발급받은 Gemini API 키를 입력해주세요.")
    api_key = st.text_input("API Key", type="password")
    st.markdown("[API 키 발급받는 곳 (무료)](https://aistudio.google.com/app/apikey)")

# 3. 메인 화면
st.title("📝 AI 마법의 문제 추출기")
st.markdown("**손글씨로 푼 문제집 사진을 올리면, 깨끗한 텍스트로 타이핑해 드립니다.**")

# 4. 사진 업로드 영역
uploaded_file = st.file_uploader("문제집 사진 업로드 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 사진", use_column_width=True)

    if st.button("✨ 텍스트 추출 시작"):
        if not api_key:
            st.error("왼쪽 사이드바에 API 키를 먼저 입력해주세요!")
        else:
            with st.spinner("AI가 손글씨를 지우고 문제를 복원하는 중입니다... 잠시만요!"):
                try:
                    # Gemini API 연결
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('models/gemini-1.5-flash')

                    # 전문가용 프롬프트
                    prompt = """
                    너는 지금부터 교육 콘텐츠 전문 편집자야. 
                    내가 업로드한 사진은 강사인 내가 직접 손으로 풀이와 정답을 적어놓은 문제집이야. 
                    학생들에게 깨끗한 상태로 배포하기 위해 아래 지침에 따라 텍스트를 추출해줘.

                    [작업 지침]
                    1. 불필요한 요소 제거: 사진 속 손글씨(풀이 과정, 정답 체크, 별표, 메모 등)는 모두 무시하고 '문제 본문'과 '보기'만 추출할 것.
                    2. 텍스트 복원: 가려지거나 흐릿한 부분은 문맥에 맞게 완벽한 문장으로 복원해줘.
                    3. 구조화: 
                       - [문제 번호]
                       - [문제 내용]
                       - [선지 1~5번] 또는 [보기 박스]
                    4. 특수기호 유지: 수학 기호, 한자, 외래어 등은 원문 그대로 유지할 것.
                    """
                    
                    # 이미지와 프롬프트를 함께 전송
                    response = model.generate_content([prompt, image])
                    
                    st.success("🎉 추출 완료!")
                    st.text_area("복사해서 한글/워드에 붙여넣으세요:", value=response.text, height=400)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다. API 키가 정확한지 확인해주세요. (상세 에러: {e})")
