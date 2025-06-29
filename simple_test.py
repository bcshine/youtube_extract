#!/usr/bin/env python3
"""
간단한 YouTube 자막 추출 테스트
"""

from youtube_transcript_api import YouTubeTranscriptApi
import json

def test_simple_extraction():
    video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    try:
        print(f"비디오 ID: {video_id}")
        print("자막 목록 가져오는 중...")
        
        # 자막 목록 가져오기
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        print(f"사용 가능한 자막: {len(list(transcript_list))}개")
        
        # 다시 목록 가져오기 (한 번 iterate하면 소진됨)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 첫 번째 자막 사용
        transcript = next(iter(transcript_list))
        print(f"선택된 자막: {transcript.language} ({transcript.language_code})")
        
        # 자막 데이터 가져오기
        transcript_data = transcript.fetch()
        print(f"자막 데이터 개수: {len(transcript_data)}개")
        
        if transcript_data:
            print("✅ 성공!")
            print(f"첫 번째 자막: {transcript_data[0].text}")
            return True
        else:
            print("❌ 자막 데이터 없음")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    test_simple_extraction() 