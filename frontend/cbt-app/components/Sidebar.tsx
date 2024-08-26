"use client";
import React from "react";
import NewSession from "./NewSession";
import ChatHistory from "./ChatHistory";
import { signOut, useSession } from "next-auth/react";
import Image from "next/image";
function Sidebar() {
  const { data: session } = useSession();

  console.log(session);
  return (
    <div className="flex flex-col h-screen p-2">
      <div className="flex-1">
        <div>
          {/* NewChat */}
          <NewSession />

          <div className="fles flex-col space-y-2 my-2">
            <ChatHistory />
          </div>
        </div>
      </div>
      {session && (
        <div className="mx-auto mb-2">
          <Image
            onClick={() => signOut()}
            className="rounded-full cursor-pointer hover:opacity-50"
            src={session.user?.image!}
            alt="User's profile picture"
            width={50} // Set your desired width
            height={50} // Set your desired height
          />
        </div>
      )}
    </div>
  );
}

export default Sidebar;
