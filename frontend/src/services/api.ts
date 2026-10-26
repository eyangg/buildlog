const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'
const TOKEN_KEY = 'buildlog_token'

export interface User {
  id: number
  email: string
  nickname: string
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface NicknameChangeResponse extends TokenResponse {
  user: User
}

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token: string | null): void {
  try {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
  } catch {
    // 저장소를 쓸 수 없으면 이번 화면에서만 로그인 상태가 유지됩니다.
  }
}

function readErrorMessage(data: unknown): string {
  if (typeof data !== 'object' || data === null || !('detail' in data)) {
    return '요청 처리에 실패했습니다. 잠시 후 다시 시도해 주세요.'
  }
  const detail = (data as { detail: unknown }).detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    const msg = String((detail[0] as { msg?: unknown }).msg ?? '')
    return msg.replace(/^Value error, /, '') || '입력값을 확인해 주세요.'
  }
  return '요청 처리에 실패했습니다. 잠시 후 다시 시도해 주세요.'
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  if (options.body !== undefined) headers.set('Content-Type', 'application/json')
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  let response: Response
  try {
    response = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해 주세요.', 0)
  }

  if (!response.ok) {
    const data: unknown = await response.json().catch(() => null)
    throw new ApiError(readErrorMessage(data), response.status)
  }
  return (await response.json()) as T
}

export const api = {
  signup: (body: { email: string; password: string; nickname: string }) =>
    request<User>('/auth/signup', { method: 'POST', body: JSON.stringify(body) }),

  login: (body: { email: string; password: string }) =>
    request<TokenResponse>('/auth/login', { method: 'POST', body: JSON.stringify(body) }),

  logout: () => request<{ message: string }>('/auth/logout', { method: 'POST' }),

  getAccountInfo: () => request<User>('/account/info'),

  changeNickname: (nickname: string) =>
    request<NicknameChangeResponse>('/account/nickname', {
      method: 'PUT',
      body: JSON.stringify({ nickname }),
    }),
}
