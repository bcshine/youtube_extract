from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import sys
import os

# 현재 스크립트 파일의 디렉토리를 Python 경로에 추가
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, '..'))

from youtube_text_extractor import YouTubeTextExtractor

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
                self.end_headers()
                response = {"success": False, "error": "URL이 필요합니다"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # YouTube 텍스트 추출
            extractor = YouTubeTextExtractor()
            extractor.use_speech_recognition = False
            
            if extractor.process_youtube_url(url):
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
                response = {
                    "success": False,
                    "error": "자막을 추출할 수 없습니다. 비디오가 비공개이거나 자막이 없을 수 있습니다."
                }
                self.send_response(400)
            
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"success": False, "error": f"서버 오류: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 