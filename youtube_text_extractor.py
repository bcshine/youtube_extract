#!/usr/bin/env python3
"""
YouTube 자막 추출기 - 안정적인 버전
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi
import requests


class YouTubeTextExtractor:
    def __init__(self):
        self.video_info = {}
        self.transcript_data = []
        self.formatted_text = ""
        self.error_details = ""
        
    def extract_video_id(self, url):
        """유튜브 URL에서 비디오 ID 추출"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/live\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_info(self, video_id):
        """비디오 정보 가져오기 - 간소화된 버전"""
        try:
            # 기본 정보만 설정
            self.video_info = {
                'title': f'Video {video_id}',
                'channel': '정보 없음',
                'duration': 0,
                'video_id': video_id
            }
        except Exception as e:
            self.video_info = {'title': '정보 없음', 'channel': '정보 없음', 'video_id': video_id}
    
    def extract_transcript(self, video_id):
        """자막 추출"""
        try:
            # 자막 목록 가져오기
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # 사용 가능한 자막 우선순위
            language_priorities = ['ko', 'en', 'en-US', 'en-GB']
            
            transcript = None
            
            # 우선순위에 따라 자막 찾기
            for lang_code in language_priorities:
                try:
                    transcript = transcript_list.find_transcript([lang_code])
                    if transcript:
                        break
                except:
                    continue
            
            # 위의 방법이 실패하면 첫 번째 사용 가능한 자막 사용
            if not transcript:
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except:
                    try:
                        # 마지막 시도: 사용 가능한 첫 번째 자막
                        available_transcripts = list(transcript_list)
                        if available_transcripts:
                            transcript = available_transcripts[0]
                    except:
                        pass
            
            # 자막 데이터 가져오기
            if transcript:
                try:
                    self.transcript_data = transcript.fetch()
                    if self.transcript_data and len(self.transcript_data) > 0:
                        return True
                except Exception as e:
                    self.error_details = f"자막 데이터 가져오기 실패: {str(e)}"
            
            return False
            
        except Exception as e:
            self.error_details = f"자막 목록 가져오기 실패: {str(e)}"
            return False
    
    def format_transcript(self):
        """자막을 읽기 쉬운 텍스트로 포맷팅"""
        if not self.transcript_data:
            return ""
        
        formatted_lines = []
        
        for entry in self.transcript_data:
            try:
                text = entry['text'].strip()
                if text and text not in ['[음악]', '[Music]', '[Applause]', '[박수]']:
                    # 줄바꿈 문자 제거 및 정리
                    text = re.sub(r'\n+', ' ', text)
                    text = re.sub(r'\s+', ' ', text)
                    formatted_lines.append(text)
            except:
                continue
        
        # 중복 제거 및 연결
        result_text = ' '.join(formatted_lines)
        
        # 문장 단위로 정리
        sentences = re.split(r'[.!?]\s+', result_text)
        formatted_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 3:
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                formatted_sentences.append(sentence)
        
        self.formatted_text = '\n\n'.join(formatted_sentences)
        return self.formatted_text
    
    def process_youtube_url(self, url):
        """메인 처리 함수"""
        try:
            # 1. 비디오 ID 추출
            video_id = self.extract_video_id(url)
            if not video_id:
                self.error_details = "올바른 유튜브 URL이 아닙니다"
                return False
            
            # 2. 비디오 정보 가져오기
            self.get_video_info(video_id)
            
            # 3. 자막 추출
            if self.extract_transcript(video_id):
                # 4. 자막 포맷팅
                self.format_transcript()
                return True
            else:
                return False
                
        except Exception as e:
            self.error_details = f"처리 중 오류: {str(e)}"
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