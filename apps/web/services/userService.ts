import { SignupResponse } from "@shared/types/user";

import { post } from "@/lib/apiClient";

export interface SignupPayload {
  email: string;
  password: string;
  goals?: Record<string, unknown> | null;
  stage: number;
}

export const userService = {
  async signup(payload: SignupPayload): Promise<SignupResponse> {
    return post<SignupResponse>("/api/v1/auth/signup", payload);
  }
};
