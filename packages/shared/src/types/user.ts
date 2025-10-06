export interface User {
  id: string;
  email: string;
  goals?: Record<string, unknown> | null;
  stage: number;
  created_at: string;
}

export interface SignupResponse {
  user: User;
  message: string;
}
