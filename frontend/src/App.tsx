import { Layout, Menu } from 'antd'
import { Link, Route, Routes } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Jobs from './pages/Jobs'
import Resume from './pages/Resume'
import Profile from './pages/Profile'

const { Header, Content, Footer } = Layout

export default function App() {
  return (
    <Layout style={{ minHeight: '100%' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ color: '#fff', fontWeight: 600, marginRight: 24 }}>Resume Helper</div>
        <Menu theme="dark" mode="horizontal" selectable={false} items={[
          { key: 'dashboard', label: <Link to="/">Dashboard</Link> },
          { key: 'jobs', label: <Link to="/jobs">Jobs</Link> },
          { key: 'resume', label: <Link to="/resume">Resume</Link> },
          { key: 'profile', label: <Link to="/profile">Profile</Link> },
        ]} />
      </Header>
      <Content style={{ padding: 24 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/resume" element={<Resume />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Content>
      <Footer style={{ textAlign: 'center' }}>© {new Date().getFullYear()} Resume Helper</Footer>
    </Layout>
  )
}

