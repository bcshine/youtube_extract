from http.server import BaseHTTPRequestHandler
import json
import re
import sys

# 인코딩 설정
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# YouTube Transcript API import
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    # 백업 응답
    class YouTubeTranscriptApi:
        @staticmethod
        def get_transcript(*args, **kwargs):
            raise Exception("youtube-transcript-api 패키지가 설치되지 않았습니다")


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


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # POST 데이터 읽기
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url')
            
            if not url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"success": False, "error": "URL이 필요합니다"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # YouTube 텍스트 추출
            extractor = YouTubeTextExtractor()
            
            if extractor.process_youtube_url(url) and extractor.formatted_text:
                response = {
                    "success": True,
                    "text": extractor.formatted_text,
                    "info": {
                        "title": extractor.video_info.get('title', '제목 없음'),
                        "channel": extractor.video_info.get('channel', '채널 없음'),
                        "duration": extractor.video_info.get('duration', 0),
                        "subtitle_count": len(extractor.transcript_data)
                    }
                }
                self.send_response(200)
            else:
                error_msg = extractor.error_details if extractor.error_details else "자막을 추출할 수 없습니다"
                
                # 구체적인 에러 메시지 제공
                if "Video unavailable" in error_msg:
                    error_msg = "비디오를 사용할 수 없습니다. 삭제되었거나 비공개일 수 있습니다."
                elif "Private video" in error_msg:
                    error_msg = "비공개 비디오입니다."
                elif "Could not retrieve a transcript" in error_msg:
                    if "Subtitles are disabled" in error_msg:
                        error_msg = "이 비디오는 자막이 비활성화되어 있습니다."
                    elif "No transcripts found" in error_msg:
                        error_msg = "이 비디오에는 자막이 없습니다."
                    else:
                        error_msg = "자막을 가져올 수 없습니다. 비디오가 제한되어 있을 수 있습니다."
                elif "Connection" in error_msg or "Network" in error_msg:
                    error_msg = "네트워크 연결 문제가 발생했습니다. 잠시 후 다시 시도해주세요."
                
                response = {
                    "success": False,
                    "error": error_msg
                }
                self.send_response(400)
            
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"success": False, "error": f"서버 오류: {str(e)}"}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 