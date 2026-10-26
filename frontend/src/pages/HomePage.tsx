import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function HomePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <main className="page">
      <h1>{user?.nickname}님의 기록</h1>
      <p>공부 기록, 할 일, 오류 기록은 다음 단계에서 추가됩니다.</p>
      <nav className="actions">
        <Link to="/settings">계정 설정</Link>
        <button type="button" onClick={handleLogout}>
          로그아웃
        </button>
      </nav>
    </main>
  )
}
