import { useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api, ApiError } from '../services/api'

export default function SettingsPage() {
  const { user, updateUser } = useAuth()

  const [nickname, setNickname] = useState(user?.nickname ?? '')
  const [message, setMessage] = useState<{ type: 'ok' | 'error'; text: string } | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setMessage(null)
    setSubmitting(true)
    try {
      const result = await api.changeNickname(nickname.trim())
      updateUser(result.user, result.access_token)
      setNickname(result.user.nickname)
      setMessage({ type: 'ok', text: '닉네임이 변경되었습니다.' })
    } catch (err) {
      setMessage({
        type: 'error',
        text: err instanceof ApiError ? err.message : '닉네임 변경에 실패했습니다.',
      })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="page narrow">
      <h1>계정 설정</h1>
      <p>현재 이메일: {user?.email}</p>
      <form onSubmit={handleSubmit} className="form">
        <label>
          닉네임 (2~20자, 한글·영문·숫자·밑줄)
          <input value={nickname} onChange={(e) => setNickname(e.target.value)} required />
        </label>
        {message && (
          <p className={message.type === 'ok' ? 'notice' : 'error'} role="alert">
            {message.text}
          </p>
        )}
        <button type="submit" disabled={submitting}>
          {submitting ? '변경 중...' : '닉네임 변경'}
        </button>
      </form>
      <p>
        <Link to="/">홈으로</Link>
      </p>
    </main>
  )
}
