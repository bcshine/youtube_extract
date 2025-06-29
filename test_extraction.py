#!/usr/bin/env python3
"""
YouTube 텍스트 추출 테스트 스크립트
"""

from youtube_text_extractor import YouTubeTextExtractor

def test_youtube_extraction():
    print("🧪 YouTube 텍스트 추출 테스트 중...")
    
    # 테스트 URL - Rick Astley "Never Gonna Give You Up"
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    extractor = YouTubeTextExtractor()
    
    print(f"📺 테스트 URL: {test_url}")
    print("🔄 텍스트 추출 중...")
    
    try:
        success = extractor.process_youtube_url(test_url)
        
        if success:
            print("✅ 성공!")
            print(f"📺 제목: {extractor.video_info.get('title', '제목 없음')}")
            print(f"👤 채널: {extractor.video_info.get('channel', '채널 없음')}")
            print(f"📝 추출된 텍스트 길이: {len(extractor.formatted_text)} 문자")
            
            # 텍스트 일부 출력
            preview = extractor.formatted_text[:200] + "..." if len(extractor.formatted_text) > 200 else extractor.formatted_text
            print(f"📋 텍스트 미리보기:\n{preview}")
            
            return True
        else:
            print("❌ 실패!")
            print(f"❗ 에러 세부사항: {extractor.error_details}")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    test_youtube_extraction() 