# 📺 유튜브 자막 추출기 (React Version)

React + Next.js로 만든 현대적인 유튜브 자막 추출 웹 애플리케이션입니다.

## ✨ 주요 기능

- 🎬 **유튜브 URL 입력**으로 간편한 자막 추출
- 📋 **원클릭 복사** 기능으로 편리한 사용
- 📱 **모바일 반응형** 디자인
- ⚡ **빠른 처리** 속도
- 🎨 **깔끔한 UI/UX**

## 🛠️ 기술 스택

### Frontend
- **React 18** - 현대적인 UI 라이브러리
- **Next.js 14** - 풀스택 React 프레임워크
- **CSS Modules** - 스타일링
- **Axios** - HTTP 클라이언트

### Backend
- **Python 3** - 자막 추출 엔진
- **youtube-transcript-api** - 유튜브 자막 API
- **yt-dlp** - 유튜브 비디오 정보

## 🚀 설치 및 실행

### 1. 필수 요구사항
```bash
# Node.js 18+ 설치 확인
node --version

# Python 3.7+ 설치 확인
python --version
```

### 2. Python 의존성 설치
```bash
pip install youtube-transcript-api yt-dlp
```

### 3. Node.js 의존성 설치
```bash
npm install
# 또는
yarn install
```

### 4. 개발 서버 실행
```bash
npm run dev
# 또는
yarn dev
```

### 5. 브라우저에서 접속
```
http://localhost:3000
```

## 📁 프로젝트 구조

```
youtube-subtitle-extractor/
├── pages/
│   ├── index.js              # 메인 페이지
│   ├── _app.js              # Next.js 앱 설정
│   └── api/
│       └── extract.js       # 자막 추출 API
├── styles/
│   ├── globals.css          # 전역 스타일
│   └── Home.module.css      # 메인 페이지 스타일
├── extract_api.py           # Python 자막 추출 스크립트
├── youtube_text_extractor.py # 기존 추출 라이브러리
├── package.json             # Node.js 설정
└── README.md               # 프로젝트 문서
```

## 🎯 사용 방법

1. **URL 입력**: 유튜브 영상 URL을 입력창에 붙여넣기
2. **자막 추출**: "📥 자막 추출" 버튼 클릭
3. **결과 확인**: 추출된 자막을 텍스트 영역에서 확인
4. **복사하기**: "📋 복사하기" 버튼으로 클립보드에 복사

## ⚠️ 지원되는 영상

### ✅ 잘 작동하는 경우
- 공개 영상 (비공개/삭제 영상 불가)
- 자막이 있는 영상 (한국어/영어 권장)
- 짧은 영상 (10분 이하 권장)
- 교육/뉴스 영상 (음성이 명확한 영상)

### ❌ 추출이 어려운 경우
- 비공개/삭제된 영상
- 지역 제한 영상
- 자막이 없는 음악 영상
- 너무 긴 영상 (1시간 이상)

## 🔧 배포

### Vercel 배포 (권장)
```bash
# Vercel CLI 설치
npm install -g vercel

# 배포
vercel
```

### 수동 빌드
```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm run start
```

## 🤝 기여하기

1. 이 저장소를 Fork
2. 새 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 문제 해결

### 자주 발생하는 문제

**Q: "Video unavailable" 오류가 발생해요**
A: 비디오가 삭제되었거나 비공개입니다. 다른 공개 영상으로 시도해보세요.

**Q: 자막이 추출되지 않아요**
A: 해당 영상에 자막이 없을 수 있습니다. 자막이 있는 영상으로 시도해보세요.

**Q: Python 스크립트 오류가 발생해요**
A: Python 의존성이 제대로 설치되었는지 확인해보세요.

---

**Made with ❤️ by YouTube Subtitle Extractor Team** 