import streamlit as st
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from youtube_text_extractor import YouTubeTextExtractor

# 페이지 설정
st.set_page_config(
    page_title="📺 YT 텍스트 추출기",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff6b6b;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #ff6b6b;
        padding: 10px 15px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b, #ee5a52);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 30px;
        font-weight: bold;
        width: 100%;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 헤더
    st.markdown('<h1 class="main-header">📺 YT 텍스트 추출기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">📝 유튜브 영상의 자막을 텍스트로 쉽게 변환하세요</p>', unsafe_allow_html=True)
    
    # URL 입력
    url = st.text_input(
        "🔗 유튜브 URL을 입력하세요",
        placeholder="https://www.youtube.com/watch?v=...",
        help="유튜브 동영상 URL을 붙여넣으세요"
    )
    
    # 음성 인식 옵션
    use_speech = st.checkbox(
        "🎤 음성 인식 모드",
        help="자막이 없는 영상의 경우 음성을 인식하여 텍스트로 변환합니다 (처리 시간이 더 오래 걸릴 수 있습니다)"
    )
    
    # 추출 버튼
    if st.button("📄 자막 추출", type="primary"):
        if not url:
            st.error("⚠️ 유튜브 URL을 입력해주세요!")
            return
        
        # URL 유효성 검사
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            st.error("⚠️ 올바른 유튜브 URL을 입력해주세요!")
            return
        
        # 진행 상태 표시
        with st.spinner('🔄 영상 정보를 가져오는 중...'):
            try:
                # 텍스트 추출 실행
                extractor = YouTubeTextExtractor()
                extractor.use_speech_recognition = use_speech
                
                success = extractor.process_youtube_url(url)
                
                if success and extractor.formatted_text:
                    # 성공 - 비디오 정보 표시
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("✅ 자막 추출 완료!")
                    
                    # 비디오 정보
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**📺 제목:** {extractor.video_info.get('title', '제목 없음')}")
                        st.write(f"**👤 채널:** {extractor.video_info.get('channel', '채널 없음')}")
                    with col2:
                        duration = extractor.video_info.get('duration', 0)
                        if duration:
                            minutes = duration // 60
                            seconds = duration % 60
                            st.write(f"**⏱️ 길이:** {minutes}분 {seconds}초")
                        st.write(f"**📝 자막 수:** {len(extractor.transcript_data)}개")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 텍스트 결과
                    st.subheader("📋 추출된 텍스트")
                    
                    # 텍스트 영역에 결과 표시
                    st.text_area(
                        "결과 (Ctrl+A로 전체 선택 후 Ctrl+C로 복사)",
                        value=extractor.formatted_text,
                        height=400,
                        help="텍스트를 선택하여 복사할 수 있습니다"
                    )
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="💾 텍스트 파일로 다운로드",
                        data=extractor.formatted_text,
                        file_name=f"{extractor.video_info.get('title', 'youtube_text')}.txt",
                        mime="text/plain"
                    )
                    
                else:
                    # 실패
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.error("❌ 자막을 추출할 수 없습니다")
                    
                    error_reasons = [
                        "🔒 비디오가 비공개이거나 삭제되었을 수 있습니다",
                        "🚫 자막이 비활성화되어 있을 수 있습니다", 
                        "🌐 네트워크 연결 문제일 수 있습니다",
                        "⏱️ 영상이 너무 길거나 처리할 수 없는 형식일 수 있습니다"
                    ]
                    
                    st.write("**가능한 원인:**")
                    for reason in error_reasons:
                        st.write(f"• {reason}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # 사용 가이드
    with st.expander("📖 사용 가이드", expanded=False):
        st.markdown("""
        ### 📝 사용 방법
        1. **유튜브 URL 입력**: 텍스트를 추출할 영상의 URL을 붙여넣으세요
        2. **옵션 선택**: 필요시 음성 인식 모드를 활성화하세요
        3. **자막 추출**: 버튼을 클릭하여 텍스트를 추출하세요
        4. **결과 복사**: 추출된 텍스트를 복사하거나 파일로 다운로드하세요
        
        ### ✅ 잘 작동하는 영상
        • 자막이 활성화된 영상
        • 공개 설정된 영상
        • 한국어/영어 콘텐츠
        
        ### ⚠️ 제한사항
        • 비공개 또는 삭제된 영상
        • 자막이 없는 영상 (음성 인식 모드 필요)
        • 매우 긴 영상 (처리 시간 오래 걸림)
        
        ### 🧪 테스트 URL
        테스트해보고 싶다면 이 URL을 사용해보세요:
        `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
        """)

if __name__ == "__main__":
    main() 