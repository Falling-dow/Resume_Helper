import { useState, useEffect, useRef } from 'react'
import { Tabs, Form, Input, Button, Typography, message } from 'antd'
import { login, register } from '@/api/auth'
import { useAuth, AuthState } from '@/store/auth'
import { useLocation, useNavigate } from 'react-router-dom'

const { Title, Text } = Typography

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const setToken = useAuth((s: AuthState) => s.setToken)
  const navigate = useNavigate()
  const location = useLocation()
  const defaultTab = location.pathname.endsWith('/register') ? 'register' : 'login'
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // 背景动画效果
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    
    const particles: Array<{
      x: number
      y: number
      size: number
      speedX: number
      speedY: number
      opacity: number
    }> = []
    
    const particleCount = 30
    
    // 创建粒子
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 1,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: (Math.random() - 0.5) * 0.5,
        opacity: Math.random() * 0.5 + 0.2
      })
    }
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      particles.forEach(particle => {
        particle.x += particle.speedX
        particle.y += particle.speedY
        
        // 边界检测
        if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1
        if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1
        
        // 绘制粒子
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(52, 211, 153, ${particle.opacity})`
        ctx.fill()
        
        // 连接附近的粒子
        particles.forEach(otherParticle => {
          const distance = Math.sqrt(
            Math.pow(particle.x - otherParticle.x, 2) + 
            Math.pow(particle.y - otherParticle.y, 2)
          )
          
          if (distance < 150) {
            ctx.beginPath()
            ctx.moveTo(particle.x, particle.y)
            ctx.lineTo(otherParticle.x, otherParticle.y)
            ctx.strokeStyle = `rgba(52, 211, 153, ${0.1 * (1 - distance / 150)})`
            ctx.stroke()
          }
        })
      })
      
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

  const onLogin = async (values: any) => {
    try {
      setLoading(true)
      const res = await login(values.email, values.password)
      setToken(res.access_token)
      message.success('登录成功')
      navigate('/')
    } catch (e: any) {
      message.error(e?.response?.data?.detail || '登录失败')
    } finally {
      setLoading(false)
    }
  }

  const onRegister = async (values: any) => {
    try {
      setLoading(true)
      const res = await register(values.email, values.password, values.username)
      setToken(res.access_token)
      message.success('注册成功，已自动登录')
      navigate('/')
    } catch (e: any) {
      message.error(e?.response?.data?.detail || '注册失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-emerald-50 via-white to-sky-50">
      {/* 背景动画画布 */}
      <canvas 
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none opacity-40"
        style={{ width: '100%', height: '100%' }}
      />
      
      {/* 装饰性背景元素 */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-20 left-20 h-72 w-72 rounded-full bg-gradient-to-br from-emerald-200/20 to-transparent blur-3xl" />
        <div className="absolute bottom-20 right-20 h-96 w-96 rounded-full bg-gradient-to-tl from-sky-200/20 to-transparent blur-3xl" />
        <div className="absolute top-1/2 left-1/2 h-80 w-80 -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-amber-100/10 to-transparent blur-3xl" />
      </div>

      {/* 主容器 */}
      <div className="relative flex min-h-screen items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          {/* Logo和标题 */}
          <div className="mb-8 text-center">
            <div className="mb-4 inline-flex items-center justify-center">
              <div className="relative">
                <div className="absolute inset-0 animate-pulse rounded-full bg-gradient-to-r from-emerald-400 to-sky-400 blur-xl opacity-50" />
                <svg width="60" height="60" viewBox="0 0 60 60" fill="none" className="relative">
                  <rect x="5" y="5" width="50" height="50" rx="12" fill="url(#logo-gradient)" />
                  <path d="M30 15 L45 30 L30 45 L15 30 Z" fill="white" fillOpacity="0.9" />
                  <defs>
                    <linearGradient id="logo-gradient" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor="#10b981" />
                      <stop offset="100%" stopColor="#0ea5e9" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
            <Title level={2} style={{ 
              margin: 0, 
              background: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: 300,
              letterSpacing: '0.05em'
            }}>
              优简智投
            </Title>
            <Text style={{ color: '#6b7280', fontSize: '16px', marginTop: '8px', display: 'block' }}>
              专属于你的智能简历优化投递助手
            </Text>
          </div>

          {/* 卡片容器 */}
          <div className="relative backdrop-blur-xl bg-white/70 rounded-3xl shadow-2xl shadow-emerald-100/50 border border-white/50 p-8">
            <Tabs
              defaultActiveKey={defaultTab}
              centered
              className="custom-auth-tabs"
              items={[
                {
                  key: 'login',
                  label: (
                    <span className="px-4 py-2 font-medium">登录</span>
                  ),
                  children: (
                    <Form 
                      layout="vertical" 
                      onFinish={onLogin} 
                      requiredMark={false}
                      className="mt-6"
                    >
                      <Form.Item 
                        name="email" 
                        label={<span style={{ color: '#374151', fontWeight: 500 }}>邮箱地址</span>} 
                        rules={[
                          { required: true, message: '请输入邮箱' },
                          { type: 'email', message: '请输入有效的邮箱地址' }
                        ]}
                      >
                        <Input 
                          size="large" 
                          placeholder="you@example.com"
                          prefix={
                            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                          }
                          className="rounded-2xl bg-white/50 backdrop-blur-sm hover:bg-white focus:bg-white transition-all"
                        />
                      </Form.Item>
                      
                      <Form.Item 
                        name="password" 
                        label={<span style={{ color: '#374151', fontWeight: 500 }}>密码</span>} 
                        rules={[{ required: true, message: '请输入密码' }]}
                      >
                        <Input.Password 
                          size="large" 
                          placeholder="••••••••"
                          prefix={
                            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                          }
                          className="rounded-2xl bg-white/50 backdrop-blur-sm hover:bg-white focus:bg-white transition-all"
                        />
                      </Form.Item>
                      
                      <div className="mb-6 flex items-center justify-between">
                        <label className="flex items-center">
                          <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                          <span className="ml-2 text-sm text-gray-600">记住我</span>
                        </label>
                        <a href="#" className="text-sm text-emerald-600 hover:text-emerald-700">
                          忘记密码？
                        </a>
                      </div>
                      
                      <Button 
                        type="primary" 
                        htmlType="submit" 
                        size="large" 
                        loading={loading} 
                        block
                        className="h-12 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 border-0 font-medium shadow-lg shadow-emerald-500/25 hover:shadow-xl hover:shadow-emerald-500/30 hover:scale-[1.02] transition-all duration-300"
                        style={{ 
                          background: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
                        }}
                      >
                        登录
                      </Button>
                    </Form>
                  ),
                },
                {
                  key: 'register',
                  label: (
                    <span className="px-4 py-2 font-medium">注册</span>
                  ),
                  children: (
                    <Form 
                      layout="vertical" 
                      onFinish={onRegister} 
                      requiredMark={false}
                      className="mt-6"
                    >
                      <Form.Item 
                        name="username" 
                        label={<span style={{ color: '#374151', fontWeight: 500 }}>昵称</span>}
                      >
                        <Input 
                          size="large" 
                          placeholder="你的昵称（可选）"
                          prefix={
                            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                          }
                          className="rounded-2xl bg-white/50 backdrop-blur-sm hover:bg-white focus:bg-white transition-all"
                        />
                      </Form.Item>
                      
                      <Form.Item 
                        name="email" 
                        label={<span style={{ color: '#374151', fontWeight: 500 }}>邮箱地址</span>} 
                        rules={[
                          { required: true, message: '请输入邮箱' },
                          { type: 'email', message: '请输入有效的邮箱地址' }
                        ]}
                      >
                        <Input 
                          size="large" 
                          placeholder="you@example.com"
                          prefix={
                            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                          }
                          className="rounded-2xl bg-white/50 backdrop-blur-sm hover:bg-white focus:bg-white transition-all"
                        />
                      </Form.Item>
                      
                      <Form.Item 
                        name="password" 
                        label={<span style={{ color: '#374151', fontWeight: 500 }}>密码</span>} 
                        rules={[
                          { required: true, message: '请输入密码' },
                          { min: 6, message: '密码至少6位字符' }
                        ]}
                      >
                        <Input.Password 
                          size="large" 
                          placeholder="至少6位字符"
                          prefix={
                            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                          }
                          className="rounded-2xl bg-white/50 backdrop-blur-sm hover:bg-white focus:bg-white transition-all"
                        />
                      </Form.Item>
                      
                      <Button 
                        type="primary" 
                        htmlType="submit" 
                        size="large" 
                        loading={loading} 
                        block
                        className="h-12 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 border-0 font-medium shadow-lg shadow-emerald-500/25 hover:shadow-xl hover:shadow-emerald-500/30 hover:scale-[1.02] transition-all duration-300"
                        style={{ 
                          background: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
                        }}
                      >
                        注册并开始
                      </Button>
                    </Form>
                  ),
                },
              ]}
            />
            
            {/* 分隔线 */}
            <div className="my-6 flex items-center">
              <div className="flex-1 border-t border-gray-200"></div>
              <span className="mx-4 text-sm text-gray-400">或</span>
              <div className="flex-1 border-t border-gray-200"></div>
            </div>
            
            {/* 第三方登录提示 */}
            <div className="text-center text-sm text-gray-500">
              邮箱/微信/QQ 登录即将上线
            </div>
          </div>
          
          {/* 底部链接 */}
          <div className="mt-8 flex justify-center space-x-6 text-sm text-gray-500">
            <a href="#" className="hover:text-emerald-600 transition-colors">服务条款</a>
            <span>•</span>
            <a href="#" className="hover:text-emerald-600 transition-colors">隐私政策</a>
            <span>•</span>
            <a href="#" className="hover:text-emerald-600 transition-colors">帮助中心</a>
          </div>
        </div>
      </div>

      {/* 自定义样式 */}
      <style>{`
        .custom-auth-tabs .ant-tabs-nav::before {
          border-bottom: none;
        }
        
        .custom-auth-tabs .ant-tabs-tab {
          color: #6b7280;
          transition: all 0.3s;
        }
        
        .custom-auth-tabs .ant-tabs-tab:hover {
          color: #10b981;
        }
        
        .custom-auth-tabs .ant-tabs-tab.ant-tabs-tab-active {
          color: #10b981;
          font-weight: 500;
        }
        
        .custom-auth-tabs .ant-tabs-ink-bar {
          background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
          height: 3px;
          border-radius: 2px;
        }
        
        .ant-input-affix-wrapper {
          border-radius: 1rem !important;
          border-color: #e5e7eb;
          transition: all 0.3s;
        }
        
        .ant-input-affix-wrapper:hover {
          border-color: #10b981;
        }
        
        .ant-input-affix-wrapper-focused {
          border-color: #10b981;
          box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
        }
        
        .ant-form-item-explain-error {
          margin-top: 0.5rem;
        }
      `}</style>
    </div>
  )
}
