#!/usr/bin/env python3
"""
YouTube 자막 추출기 - React 앱용 간소화 버전
"""

import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp


class YouTubeTextExtractor:
    def __init__(self):
        self.video_info = {}
        self.transcript_data = []
        self.formatted_text = ""
        self.use_speech_recognition = False  # React 앱에서는 비활성화
        self.error_details = ""  # 에러 세부정보 저장
        
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
        """비디오 정보 가져오기"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                
                self.video_info = {
                    'title': info.get('title', '제목 없음'),
                    'channel': info.get('uploader', '채널 없음'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', ''),
                    'video_id': video_id
                }
                
        except Exception as e:
            self.video_info = {'title': '정보 없음', 'channel': '정보 없음', 'video_id': video_id}
    
    def extract_transcript(self, video_id):
        """자막 추출 - 개선된 버전"""
        try:
            # 자막 목록 가져오기
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # 사용 가능한 자막 우선순위 리스트
            language_priorities = [
                ('ko', False),  # 수동 한국어
                ('en', False),  # 수동 영어
                ('ko', True),   # 자동 한국어
                ('en', True),   # 자동 영어
                ('en-US', True), # 자동 미국 영어
                ('en-GB', True), # 자동 영국 영어
            ]
            
            transcript = None
            
            # 우선순위에 따라 자막 찾기
            for lang_code, is_generated in language_priorities:
                try:
                    for t in transcript_list:
                        if (t.language_code == lang_code and 
                            t.is_generated == is_generated):
                            transcript = t
                            break
                    if transcript:
                        break
                except:
                    continue
            
            # 위의 방법이 모두 실패하면 사용 가능한 첫 번째 자막 사용
            if not transcript:
                try:
                    # 모든 자막을 순회하며 첫 번째 사용 가능한 것 선택
                    for t in transcript_list:
                        try:
                            transcript = t
                            break
                        except:
                            continue
                except:
                    pass
            
            # 자막 데이터 가져오기
            if transcript:
                try:
                    self.transcript_data = transcript.fetch()
                    if self.transcript_data and len(self.transcript_data) > 0:
                        return True
                except:
                    # 번역 시도 (한국어로)
                    try:
                        translated = transcript.translate('ko')
                        self.transcript_data = translated.fetch()
                        if self.transcript_data and len(self.transcript_data) > 0:
                            return True
                    except:
                        # 원본 자막 그대로 사용
                        try:
                            self.transcript_data = transcript.fetch()
                            if self.transcript_data and len(self.transcript_data) > 0:
                                return True
                        except:
                            pass
            
            return False
            
        except Exception as e:
            # 더 구체적인 에러 정보 저장
            self.error_details = str(e)
            return False
    
    def format_transcript(self):
        """자막을 읽기 쉬운 텍스트로 포맷팅"""
        if not self.transcript_data:
            return ""
        
        formatted_lines = []
        
        for entry in self.transcript_data:
            text = entry.text.strip()
            if text and text not in ['[음악]', '[Music]', '[Applause]', '[박수]']:
                # 줄바꿈 문자 제거 및 정리
                text = re.sub(r'\n+', ' ', text)
                text = re.sub(r'\s+', ' ', text)
                formatted_lines.append(text)
        
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
                raise ValueError("올바른 유튜브 URL이 아닙니다")
            
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
            return False


def main():
    """테스트용 메인 함수"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    extractor = YouTubeTextExtractor()
    
    if extractor.process_youtube_url(url):
        # 성공적으로 추출됨
        pass
    else:
        # 추출 실패
        pass


if __name__ == "__main__":
    main() 