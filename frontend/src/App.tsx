import { Layout } from 'antd'
import { Link, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Jobs from './pages/Jobs'
import Resume from './pages/Resume'
import Profile from './pages/Profile'
import LoginPage from './pages/Auth/Login'
import { useAuth } from './store/auth'
import Home from './pages/Home'

const { Header, Content, Footer } = Layout

export default function App() {
  const token = useAuth((s) => s.token)
  const logout = useAuth((s) => s.logout)
  const navigate = useNavigate()
  const location = useLocation()
  const isHome = location.pathname === '/'
  const isAuth = location.pathname.startsWith('/auth')
  const menuItems = isHome
    ? []
    : [
        { key: 'home', label: <Link to="/">首页</Link> },
        { key: 'dashboard', label: <Link to="/dashboard">Dashboard</Link> },
        { key: 'jobs', label: <Link to="/jobs">Jobs</Link> },
        { key: 'resume', label: <Link to="/resume">Resume</Link> },
        { key: 'profile', label: <Link to="/profile">Profile</Link> },
      ]
  return (
    <Layout style={{ minHeight: '100vh', background: 'transparent' }}>
      {/* Header removed globally per request */}
      <Content style={{ padding: (isHome || isAuth) ? 0 : 24, background: 'transparent' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/resume" element={<Resume />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/register" element={<LoginPage />} />
        </Routes>
      </Content>
      <Footer style={{ textAlign: 'center', background: 'transparent', display: (isHome || isAuth) ? 'none' as const : 'block' }}>© {new Date().getFullYear()} 轻简</Footer>
    </Layout>
  )
}
