import React, { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Home() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const navigate = useNavigate()
  
  // 模拟导航函数
  const handleNavigation = (path: string) => {
    navigate(path)
  }
  
  // 动画铅笔效果（在大书卷/简历纸张上书写）
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    
    // 纸张尺寸与位置（自适应）
    const paperW = Math.min(520, canvas.width * 0.5)
    const paperH = Math.min(680, canvas.height * 0.75)
    const paperX = (canvas.width - paperW) / 2
    const paperY = (canvas.height - paperH) / 2
    const margin = 32
    const lineSpacing = 26
    const lineStartY = paperY + 80
    const lineCount = Math.max(6, Math.floor((paperH - 120) / lineSpacing))

    let progress = 0 // 书写进度（像素）
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // 绘制大书卷/纸张
      const r = 24
      ctx.save()
      ctx.shadowColor = 'rgba(2, 6, 23, 0.12)'
      ctx.shadowBlur = 24
      ctx.shadowOffsetY = 12
      ctx.fillStyle = 'rgba(255,255,255,0.92)'
      ctx.beginPath()
      // 圆角矩形路径
      ctx.moveTo(paperX + r, paperY)
      ctx.lineTo(paperX + paperW - r, paperY)
      ctx.quadraticCurveTo(paperX + paperW, paperY, paperX + paperW, paperY + r)
      ctx.lineTo(paperX + paperW, paperY + paperH - r)
      ctx.quadraticCurveTo(paperX + paperW, paperY + paperH, paperX + paperW - r, paperY + paperH)
      ctx.lineTo(paperX + r, paperY + paperH)
      ctx.quadraticCurveTo(paperX, paperY + paperH, paperX, paperY + paperH - r)
      ctx.lineTo(paperX, paperY + r)
      ctx.quadraticCurveTo(paperX, paperY, paperX + r, paperY)
      ctx.closePath()
      ctx.fill()
      ctx.restore()

      // 顶部与底部卷边轻微高光
      const gradTop = ctx.createLinearGradient(0, paperY, 0, paperY + 40)
      gradTop.addColorStop(0, 'rgba(226,232,240,0.65)')
      gradTop.addColorStop(1, 'rgba(226,232,240,0.0)')
      ctx.fillStyle = gradTop
      ctx.fillRect(paperX + 8, paperY + 8, paperW - 16, 36)

      const gradBottom = ctx.createLinearGradient(0, paperY + paperH - 40, 0, paperY + paperH)
      gradBottom.addColorStop(0, 'rgba(226,232,240,0.0)')
      gradBottom.addColorStop(1, 'rgba(226,232,240,0.45)')
      ctx.fillStyle = gradBottom
      ctx.fillRect(paperX + 8, paperY + paperH - 44, paperW - 16, 36)

      // 纸张内容虚线/横线
      ctx.strokeStyle = 'rgba(2, 6, 23, 0.08)'
      ctx.lineWidth = 1
      for (let i = 0; i < lineCount; i++) {
        const y = lineStartY + i * lineSpacing
        ctx.beginPath()
        ctx.moveTo(paperX + margin, y)
        ctx.lineTo(paperX + paperW - margin, y)
        ctx.stroke()
      }

      // 计算当前书写位置
      const rowWidth = paperW - margin * 2 - 20
      const row = Math.floor(progress / rowWidth)
      const x = paperX + margin + (progress % rowWidth)
      const y = lineStartY + (row % lineCount) * lineSpacing

      // 书写轨迹
      ctx.strokeStyle = 'rgba(34, 197, 94, 0.35)'
      ctx.lineWidth = 1.6
      ctx.beginPath()
      ctx.moveTo(Math.max(paperX + margin, x - 80), y)
      for (let i = 0; i < 40; i++) {
        const px = Math.max(paperX + margin, x - 80) + i * 2
        if (px > x) break
        const py = y + Math.sin((progress * 0.01 + i * 0.3)) * 1.2
        ctx.lineTo(px, py)
      }
      ctx.stroke()

      // 绘制铅笔
      const pencilAngle = -Math.PI / 10 + Math.sin(progress * 0.01) * 0.03

      ctx.save()
      ctx.translate(x, y)
      ctx.rotate(pencilAngle)
      
      // 铅笔主体
      ctx.fillStyle = 'rgba(251, 191, 36, 0.85)'
      ctx.fillRect(-60, -3, 60, 6)
      
      // 铅笔尖
      ctx.fillStyle = 'rgba(107, 114, 128, 0.8)'
      ctx.beginPath()
      ctx.moveTo(0, -3)
      ctx.lineTo(12, 0)
      ctx.lineTo(0, 3)
      ctx.closePath()
      ctx.fill()
      
      // 橡皮擦
      ctx.fillStyle = 'rgba(239, 68, 68, 0.85)'
      ctx.fillRect(-70, -3, 10, 6)
      
      ctx.restore()
      
      progress = (progress + 2) % (rowWidth * lineCount)
      requestAnimationFrame(animate)
    }
    
    animate()
    
    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-emerald-50 via-white to-sky-50">
      {/* 动画画布 */}
      <canvas 
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none opacity-60"
      />
      
      {/* 装饰性背景元素 */}
      <div className="absolute inset-0 pointer-events-none">
        {/* 渐变圆形装饰 */}
        <div className="absolute top-20 left-10 h-64 w-64 rounded-full bg-gradient-to-br from-emerald-200/30 to-transparent blur-3xl" />
        <div className="absolute bottom-20 right-10 h-80 w-80 rounded-full bg-gradient-to-tl from-sky-200/30 to-transparent blur-3xl" />
        <div className="absolute top-1/2 left-1/3 h-96 w-96 rounded-full bg-gradient-to-r from-amber-100/20 to-transparent blur-3xl" />
        
        {/* 装饰性图标 */}
        <svg className="absolute top-32 right-1/4 h-8 w-8 text-emerald-300/30 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
          <path fillRule="evenodd" d="M4 5a2 2 0 012-2 1 1 0 000 2H6a2 2 0 100 4h2a2 2 0 100 4H6a1 1 0 100 2 2 2 0 01-2-2V5z" clipRule="evenodd" />
        </svg>
        
        <svg className="absolute bottom-40 left-1/4 h-10 w-10 text-sky-300/30 animate-bounce" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
          <path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z" />
        </svg>
        
        <div className="absolute top-1/3 left-20 h-3 w-3 rounded-full bg-emerald-400/40 animate-ping" />
        <div className="absolute bottom-1/3 right-32 h-4 w-4 rounded-full bg-sky-400/40 animate-ping" style={{animationDelay: '1s'}} />
      </div>

      {/* 主要内容 */}
      <div className="relative flex min-h-screen flex-col items-center justify-center px-6">
        {/* 主标题 - 艺术字体 */}
        <h1 className="mb-8 select-none">
          <span className="relative inline-block text-7xl md:text-8xl lg:text-9xl font-thin tracking-wider">
            <span className="bg-gradient-to-r from-emerald-600 via-teal-500 to-sky-600 bg-clip-text text-transparent drop-shadow-sm">
              优简
            </span>
            <span className="bg-gradient-to-r from-sky-600 via-blue-500 to-indigo-600 bg-clip-text text-transparent drop-shadow-sm">
              智投
            </span>
            {/* 装饰性下划线 */}
            <svg className="absolute -bottom-2 left-0 w-full" height="12" viewBox="0 0 300 12">
              <path
                d="M10,8 Q150,2 290,8"
                stroke="url(#gradient-underline)"
                strokeWidth="2"
                fill="none"
                strokeLinecap="round"
                opacity="0.6"
              />
              <defs>
                <linearGradient id="gradient-underline" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#10b981" />
                  <stop offset="50%" stopColor="#14b8a6" />
                  <stop offset="100%" stopColor="#0ea5e9" />
                </linearGradient>
              </defs>
            </svg>
          </span>
        </h1>

        {/* 副标题 - 弧形排列 */}
        <div className="relative mb-12 h-20">
          <svg width="480" height="90" viewBox="0 0 480 90" className="absolute left-1/2 top-0 -translate-x-1/2">
            <defs>
              <path id="curve" d="M 60 55 Q 240 20 420 55" />
              <linearGradient id="text-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#34d399" />
                <stop offset="50%" stopColor="#22d3ee" />
                <stop offset="100%" stopColor="#60a5fa" />
              </linearGradient>
            </defs>
            <text fill="url(#text-gradient)" fontSize="20" fontWeight="600" letterSpacing="2" fontFamily="ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,PingFang SC,Hiragino Sans GB,Microsoft YaHei,sans-serif">
              <textPath href="#curve" startOffset="50%" textAnchor="middle">
                专属于你的智能简历优化投递助手
              </textPath>
            </text>
            
            {/* 装饰性星星 */}
            <circle cx="40" cy="52" r="2" fill="#fbbf24" opacity="0.6" className="animate-pulse" />
            <circle cx="440" cy="52" r="2" fill="#fbbf24" opacity="0.6" className="animate-pulse" style={{animationDelay: '0.5s'}} />
          </svg>
        </div>

        {/* 操作按钮 */}
        <div className="mt-8 flex flex-col sm:flex-row items-center gap-4">
          <button
            onClick={() => handleNavigation('/auth/register')}
            className="group relative px-8 py-4 text-lg font-medium text-white transition-all duration-300 hover:scale-105"
          >
            <span className="absolute inset-0 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 shadow-lg shadow-emerald-500/25"></span>
            <span className="absolute inset-0 rounded-full bg-gradient-to-r from-emerald-600 to-teal-600 opacity-0 transition-opacity group-hover:opacity-100"></span>
            <span className="relative flex items-center gap-2">
              立即开始
              <svg className="h-5 w-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
          </button>
          
          <button
            onClick={() => handleNavigation('/auth/login')}
            className="group relative px-8 py-4 text-lg font-medium transition-all duration-300 hover:scale-105"
          >
            <span className="absolute inset-0 rounded-full border-2 border-gray-300 bg-white/80 backdrop-blur-sm"></span>
            <span className="absolute inset-0 rounded-full border-2 border-emerald-400 bg-emerald-50 opacity-0 transition-opacity group-hover:opacity-100"></span>
            <span className="relative flex items-center gap-2 text-gray-700 group-hover:text-emerald-700">
              登录
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
            </span>
          </button>
        </div>

        {/* 底部装饰文字 */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-center">
          <p className="text-sm text-gray-400">
            让每一份简历都能精准触达
          </p>
        </div>
      </div>
    </div>
  )
}
