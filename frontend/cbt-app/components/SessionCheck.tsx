"use client";

import { useSession } from "next-auth/react";
import Login from "./Login";
import { Session } from "next-auth";
import { LoaderCircle } from "lucide-react";

// Client-side session check component
export function SessionCheck({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return (
      <div className="flex flex-col text-white font-bold h-screen justify-center items-center">
        <LoaderCircle />
        Loading.....
      </div>
    );
  }

  if (!session) {
    return <Login />;
  }

  return <>{children}</>;
}
