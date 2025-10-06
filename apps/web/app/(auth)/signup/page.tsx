"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

import { userService } from "@/services/userService";
import { useAuthStore } from "@/stores/authStore";

const passwordPolicy = z
  .string()
  .min(8, "Password must contain at least 8 characters")
  .regex(/[A-Z]/, "Include at least one uppercase letter")
  .regex(/[a-z]/, "Include at least one lowercase letter")
  .regex(/\d/, "Include at least one number");

const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: passwordPolicy,
  goals: z.string().optional(),
  stage: z.coerce.number().min(1).max(3).default(1),
  consent: z.boolean().refine((value) => value, "Consent is required")
});

export type SignupFormValues = z.infer<typeof schema>;

export default function SignupPage(): JSX.Element {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<SignupFormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      stage: 1,
      consent: false
    }
  });

  const setUser = useAuthStore((state) => state.setUser);
  const [apiError, setApiError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const onSubmit = handleSubmit(async (values) => {
    setApiError(null);
    setSuccess(null);
    try {
      const goalsPayload = values.goals ? { summary: values.goals } : undefined;
      const response = await userService.signup({
        email: values.email,
        password: values.password,
        goals: goalsPayload,
        stage: values.stage
      });
      setUser(response.user);
      setSuccess(response.message);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Unable to create account");
    }
  });

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-lg flex-col justify-center gap-6 p-8">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-semibold text-slate-50">Create your Noria account</h1>
        <p className="text-sm text-slate-300">
          Start tracking goals and conversations with tailored coaching insights.
        </p>
      </div>
      <form onSubmit={onSubmit} className="space-y-4 rounded-lg bg-slate-900 p-6 shadow-lg">
        <div className="flex flex-col gap-1">
          <label htmlFor="email" className="text-sm font-medium text-slate-100">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="rounded-md border border-slate-700 bg-slate-950 p-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            {...register("email")}
          />
          {errors.email && <p className="text-sm text-rose-400">{errors.email.message}</p>}
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="password" className="text-sm font-medium text-slate-100">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="rounded-md border border-slate-700 bg-slate-950 p-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            {...register("password")}
          />
          {errors.password && <p className="text-sm text-rose-400">{errors.password.message}</p>}
          <p className="text-xs text-slate-400">
            Must be at least 8 characters and contain upper, lower, and numeric characters.
          </p>
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="goals" className="text-sm font-medium text-slate-100">
            Goals (optional)
          </label>
          <textarea
            id="goals"
            rows={3}
            className="rounded-md border border-slate-700 bg-slate-950 p-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            placeholder="Tell us what you want to focus on"
            {...register("goals")}
          />
          {errors.goals && <p className="text-sm text-rose-400">{errors.goals.message}</p>}
        </div>

        <div className="flex items-center gap-2">
          <input
            id="consent"
            type="checkbox"
            className="h-4 w-4 rounded border-slate-700 bg-slate-950 text-indigo-500 focus:ring-indigo-500"
            {...register("consent")}
          />
          <label htmlFor="consent" className="text-sm text-slate-200">
            I agree to the privacy policy and understand how my data is used.
          </label>
        </div>
        {errors.consent && <p className="text-sm text-rose-400">{errors.consent.message}</p>}

        <div className="flex flex-col gap-2">
          <label htmlFor="stage" className="text-sm font-medium text-slate-100">
            Current stage
          </label>
          <select
            id="stage"
            className="rounded-md border border-slate-700 bg-slate-950 p-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            {...register("stage")}
          >
            <option value={1}>Stage 1 – Getting Started</option>
            <option value={2}>Stage 2 – Building Momentum</option>
            <option value={3}>Stage 3 – Thriving</option>
          </select>
          {errors.stage && <p className="text-sm text-rose-400">{errors.stage.message}</p>}
        </div>

        <button
          type="submit"
          className="w-full rounded-md bg-indigo-500 py-2 text-sm font-semibold text-white hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-slate-700"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Creating account..." : "Create account"}
        </button>
      </form>
      {apiError && <p className="text-sm text-rose-400">{apiError}</p>}
      {success && <p className="text-sm text-emerald-400">{success}</p>}
    </main>
  );
}
