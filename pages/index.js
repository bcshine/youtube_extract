import { useState } from 'react';
import axios from 'axios';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [url, setUrl] = useState('');
  const [subtitles, setSubtitles] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);

  // 유튜브 URL 유효성 검사
  const isValidYouTubeUrl = (url) => {
    const pattern = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/live\/)([^&\n?#]+)/;
    return pattern.test(url);
  };

  // 자막 추출 함수
  const extractSubtitles = async () => {
    if (!url.trim()) {
      setError('유튜브 URL을 입력해주세요');
      return;
    }

    if (!isValidYouTubeUrl(url)) {
      setError('올바른 유튜브 URL을 입력해주세요');
      return;
    }

    setLoading(true);
    setError('');
    setSubtitles('');
    setVideoInfo(null);

    try {
      const response = await axios.post('/api/extract', { url });
      
      if (response.data.success) {
        setSubtitles(response.data.text);
        setVideoInfo(response.data.info);
      } else {
        setError(response.data.error || '자막을 추출할 수 없습니다');
      }
    } catch (err) {
      setError('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 클립보드 복사 함수
  const copyToClipboard = async () => {
    if (!subtitles) return;

    try {
      await navigator.clipboard.writeText(subtitles);
      alert('자막이 클립보드에 복사되었습니다!');
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = subtitles;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      alert('자막이 클립보드에 복사되었습니다!');
    }
  };

  // 엔터키 처리
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      extractSubtitles();
    }
  };

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          📺 유튜브 자막 추출기
        </h1>
        
        <p className={styles.description}>
          🎬 유튜브 영상의 자막을 텍스트로 쉽게 변환하세요
        </p>

        <div className={styles.inputSection}>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            className={styles.urlInput}
            disabled={loading}
          />
          
          <button 
            onClick={extractSubtitles}
            disabled={loading}
            className={styles.extractButton}
          >
            {loading ? '⏳ 추출 중...' : '📥 자막 추출'}
          </button>
        </div>

        {error && (
          <div className={styles.error}>
            ❌ {error}
          </div>
        )}

        {videoInfo && (
          <div className={styles.videoInfo}>
            🎬 <strong>{videoInfo.title}</strong>
          </div>
        )}

        {subtitles && (
          <div className={styles.resultSection}>
            <div className={styles.resultHeader}>
              <h3>📄 추출된 자막</h3>
              <button 
                onClick={copyToClipboard}
                className={styles.copyButton}
              >
                📋 복사하기
              </button>
            </div>
            
            <textarea
              value={subtitles}
              readOnly
              className={styles.subtitleArea}
              placeholder="자막이 여기에 표시됩니다..."
            />
          </div>
        )}

        <div className={styles.footer}>
          <p>💡 <strong>팁:</strong> 공개된 영상의 URL을 입력하세요</p>
        </div>
      </main>
    </div>
  );
} 