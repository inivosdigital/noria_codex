import { create } from "zustand";

import type { User } from "@shared/types/user";

interface AuthState {
  user: User | null;
  setUser: (user: User) => void;
  clear: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clear: () => set({ user: null })
}));
