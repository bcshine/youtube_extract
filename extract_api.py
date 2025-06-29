#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 자막 추출 API 스크립트
React 프론트엔드에서 호출되는 백엔드 스크립트
"""

import sys
import json
import os

# 현재 스크립트 파일의 디렉토리를 Python 경로에 추가
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from youtube_text_extractor import YouTubeTextExtractor

def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "success": False,
            "error": "URL 매개변수가 필요합니다"
        }))
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        # 추출기 생성
        extractor = YouTubeTextExtractor()
        extractor.use_speech_recognition = False  # API에서는 빠른 처리를 위해 비활성화
        
        # 자막 추출 시도
        result_file = extractor.process_youtube_url(url)
        
        if result_file and extractor.formatted_text:
            # 성공적으로 추출됨
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
        else:
            # 추출 실패
            response = {
                "success": False,
                "error": "자막을 추출할 수 없습니다. 비디오가 비공개이거나 자막이 없을 수 있습니다."
            }
            
    except Exception as e:
        error_msg = str(e)
        
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
        else:
            error_msg = f"오류가 발생했습니다: {error_msg}"
        
        response = {
            "success": False,
            "error": error_msg
        }
    
    # JSON 응답 출력
    try:
        json_output = json.dumps(response, ensure_ascii=False, indent=None, separators=(',', ':'))
        print(json_output)
        sys.stdout.flush()
    except Exception as e:
        # 백업 응답
        backup_response = {"success": False, "error": "JSON encoding error"}
        print(json.dumps(backup_response))
        sys.stdout.flush()

if __name__ == "__main__":
    main() 