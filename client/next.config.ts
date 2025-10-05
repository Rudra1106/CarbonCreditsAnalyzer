import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb'
    },
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination:
          "https://carboncreditsanalyzer-production.up.railway.app/:path*", 
      },
    ];
  },
}

export default nextConfig
