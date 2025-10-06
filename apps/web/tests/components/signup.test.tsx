import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import SignupPage from "@/app/(auth)/signup/page";
import { userService } from "@/services/userService";
import { useAuthStore } from "@/stores/authStore";

vi.mock("@/services/userService", () => ({
  userService: {
    signup: vi.fn()
  }
}));

describe("SignupPage", () => {
  beforeEach(() => {
    useAuthStore.setState({ user: null });
    vi.resetAllMocks();
  });

  it("shows validation error when password policy is violated", async () => {
    render(<SignupPage />);

    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: "test@example.com" } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: "weak" } });
    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    expect(await screen.findByText(/Password must contain at least 8 characters/i)).toBeInTheDocument();
  });

  it("submits signup form and stores user on success", async () => {
    const mockUser = {
      user: {
        id: "123",
        email: "success@example.com",
        goals: null,
        stage: 1,
        created_at: new Date().toISOString()
      },
      message: "Account created"
    };
    vi.mocked(userService.signup).mockResolvedValue(mockUser);

    render(<SignupPage />);

    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: "success@example.com" }
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "Password123" }
    });
    fireEvent.click(screen.getByLabelText(/I agree/i));
    fireEvent.change(screen.getByLabelText(/Current stage/i), { target: { value: '2' } });

    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /create account/i }));
    });

    await waitFor(() => expect(userService.signup).toHaveBeenCalled());
    expect(await screen.findByText(/Account created/i)).toBeInTheDocument();

    const state = useAuthStore.getState();
    expect(state.user?.email).toEqual("success@example.com");
  });
});
