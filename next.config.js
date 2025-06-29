/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // 환경별 설정
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  
  // 정적 파일 최적화
  images: {
    formats: ['image/webp', 'image/avif'],
  },
}

module.exports = nextConfig 