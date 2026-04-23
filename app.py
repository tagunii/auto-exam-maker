import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 앱 설정
st.set_page_config(page_title="문제집 텍스트 복원기", page_icon="📝")

with st.sidebar:
    st.header("⚙️ 환경 설정")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("API 키를 입력해야 작동합니다.")

st.title("📝 AI 문제집 복원기")
st.markdown("낙서가 있는 이미지를 문제집 원본으로 변환합니다.")

uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드됨", use_container_width=True)

    if st.button("✨ 텍스트 추출 시작"):
        if not api_key:
            st.error("API 키를 입력해주세요!")
        else:
            with st.spinner("AI 엔진 가동 중..."):
                try:
                    # [핵심 수정] API 버전을 v1으로 명시하고 라이브러리를 초기화합니다.
                    genai.configure(api_key=api_key)
                    
                    # 가장 호환성이 높은 모델 명칭을 사용합니다.
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

                    prompt = """
                    이미지 속의 모든 손글씨(풀이, 정답 체크, 메모)를 무시하고, 
                    원래 인쇄되어 있던 '문제'와 '보기'만 정확히 텍스트로 추출해줘.
                    출력 형식:
                    [문제 번호]
                    내용...
                    1) ... 2) ...
                    """
                    
                    # 콘텐츠 생성 시 안전하게 호출
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        st.success("🎉 추출 완료!")
                        st.text_area("복사해서 사용하세요:", value=response.text, height=400)
                    else:
                        st.warning("텍스트를 추출하지 못했습니다. 사진을 더 선명하게 찍어주세요.")
                        
                except Exception as e:
                    # 에러 메시지를 더 구체적으로 파악하기 위한 디버깅 메시지
                    st.error(f"시스템 연결 오류: {str(e)}")
                    st.info("도움말: API 키가 'Google AI Studio'에서 생성된 최신 키인지 확인해주세요.")
