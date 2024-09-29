"use client";
import React from "react";
import { signIn } from "next-auth/react";
import Image from "next/image";
import img1 from "../images/img2.jpeg";
import { useSession } from "next-auth/react";

function Login() {
  const { data: session } = useSession();
  console.log("SESSION===>>>", session);
  !session ? console.log("no session") : console.log("session");
  return (
    <div className="bg-white h-screen flex flex-col justify-center items-center text-center">
      <Image
        src={img1}
        width={300}
        height={300}
        className="rounded-md"
        alt=""
      />
      <button
        onClick={() => signIn("google")}
        className="text-red-900 font-bold text-3xl animate-pulse mt-6"
      >
        Signin to start therapy session
      </button>
    </div>
  );
}

export default Login;
