import { spawn } from 'child_process';
import path from 'path';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  // 유튜브 URL 유효성 검사
  const urlPattern = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/live\/)([^&\n?#]+)/;
  if (!urlPattern.test(url)) {
    return res.status(400).json({ error: '올바른 유튜브 URL을 입력해주세요' });
  }

  try {
    // Python 스크립트 실행
    const pythonScript = path.join(process.cwd(), 'extract_api.py');
    
    const pythonProcess = spawn('python', [pythonScript, url]);
    
    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      clearTimeout(timeout); // 타임아웃 클리어
      if (res.headersSent) return; // 이미 응답이 전송된 경우 중복 방지
      
      if (code === 0) {
        try {
          console.log('Python 출력:', stdout);
          const result = JSON.parse(stdout);
          
          if (result.success) {
            return res.status(200).json({
              success: true,
              text: result.text,
              info: result.info
            });
          } else {
            return res.status(400).json({
              success: false,
              error: result.error || '자막을 추출할 수 없습니다'
            });
          }
        } catch (parseError) {
          console.error('JSON 파싱 오류:', parseError);
          console.error('원본 출력:', stdout);
          return res.status(500).json({
            success: false,
            error: '서버에서 응답을 처리하는 중 오류가 발생했습니다'
          });
        }
      } else {
        console.error('Python 스크립트 오류:', stderr);
        return res.status(500).json({
          success: false,
          error: 'Python 스크립트 실행 중 오류가 발생했습니다'
        });
      }
    });

    // 타임아웃 설정 (60초)
    const timeout = setTimeout(() => {
      if (!res.headersSent) {
        pythonProcess.kill();
        return res.status(408).json({
          success: false,
          error: '요청 시간이 초과되었습니다. 짧은 영상으로 다시 시도해주세요.'
        });
      }
    }, 60000);



  } catch (error) {
    console.error('API 오류:', error);
    res.status(500).json({
      success: false,
      error: '서버 오류가 발생했습니다'
    });
  }
} 