"use client";

import { useSession } from "next-auth/react";
import Login from "./Login";
import { Session } from "next-auth";

// Client-side session check component
export function SessionCheck({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <Login />;
  }

  return <>{children}</>;
}
