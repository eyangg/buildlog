import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, ApiError } from '../services/api'

export default function SignupPage() {
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [nickname, setNickname] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await api.signup({ email: email.trim(), password, nickname: nickname.trim() })
      navigate('/login', { state: { notice: '회원가입이 완료되었습니다. 로그인해 주세요.' } })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '회원가입에 실패했습니다.')
      setPassword('')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="page narrow">
      <h1>회원가입</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          이메일
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          닉네임 (2~20자, 한글·영문·숫자·밑줄)
          <input value={nickname} onChange={(e) => setNickname(e.target.value)} required />
        </label>
        <label>
          비밀번호 (8~64자)
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <p className="error" role="alert">{error}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? '가입 중...' : '회원가입'}
        </button>
      </form>
      <p>
        이미 계정이 있나요? <Link to="/login">로그인</Link>
      </p>
    </main>
  )
}
