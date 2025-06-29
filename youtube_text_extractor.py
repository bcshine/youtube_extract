#!/usr/bin/env python3
"""
YouTube 자막 추출기 - 초간단 버전
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTextExtractor:
    def __init__(self):
        self.video_info = {}
        self.transcript_data = []
        self.formatted_text = ""
        self.error_details = ""
        
    def extract_video_id(self, url):
        """유튜브 URL에서 비디오 ID 추출"""
        match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', url)
        return match.group(1) if match else None
    
    def get_video_info(self, video_id):
        """기본 비디오 정보 설정"""
        self.video_info = {
            'title': f'YouTube Video {video_id}',
            'channel': 'Unknown',
            'duration': 0,
            'video_id': video_id
        }
    
    def extract_transcript(self, video_id):
        """자막 추출"""
        try:
            # 한국어 자막 시도
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
            except:
                # 영어 자막 시도
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                except:
                    # 사용 가능한 모든 자막 시도
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            self.transcript_data = transcript
            return True if transcript else False
            
        except Exception as e:
            self.error_details = str(e)
            return False
    
    def format_transcript(self):
        """자막 포맷팅"""
        if not self.transcript_data:
            return ""
        
        texts = []
        for entry in self.transcript_data:
            text = entry.get('text', '').strip()
            if text:
                texts.append(text)
        
        self.formatted_text = ' '.join(texts)
        return self.formatted_text
    
    def process_youtube_url(self, url):
        """메인 처리 함수"""
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                self.error_details = "올바른 유튜브 URL이 아닙니다"
                return False
            
            self.get_video_info(video_id)
            
            if self.extract_transcript(video_id):
                self.format_transcript()
                return True
            else:
                return False
                
        except Exception as e:
            self.error_details = str(e)
            return False


def main():
    """테스트용 메인 함수"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    extractor = YouTubeTextExtractor()
    
    if extractor.process_youtube_url(url):
        print("성공!")
        print(extractor.formatted_text[:200])
    else:
        print("실패!")
        print(extractor.error_details)


if __name__ == "__main__":
    main() 