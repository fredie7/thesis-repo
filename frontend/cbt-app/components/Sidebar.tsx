"use client";
import React from "react";
import NewSession from "./NewSession";
import ChatHistory from "./ChatHistory";
import { signOut, useSession } from "next-auth/react";
import Image from "next/image";
import { useCollection } from "react-firebase-hooks/firestore";
import { collection, orderBy, query } from "firebase/firestore";
import { db } from "@/firebase";
import SessionRow from "./SessionRow";
import { useSelector } from "react-redux";
function Sidebar() {
  const { data: session } = useSession();
  const sidebarVisible = useSelector(
    (state: any) => state.toggle.sidebarVisible
  );
  console.log("sidebarVisible===>>s", sidebarVisible);
  // const [chats, loading, error] = useCollection(
  //   session && collection(db, "users", session?.user?.email!, "chats")
  // );
  const [chats, loading, error] = useCollection(
    session &&
      query(
        collection(db, "users", session?.user?.email!, "chats"),
        orderBy("createdAt", "asc")
      )
  );
  console.log(chats);

  return (
    <div className="flex flex-col h-screen p-2 bg-gray-100">
      <div className="flex-1">
        <div>
          {/* NewChat */}
          <NewSession />

          {chats?.docs.map((chat) => (
            <SessionRow key={chat.id} id={chat.id} />
          ))}
        </div>
      </div>

      {session ? (
        <div className="mx-auto mb-2">
          <Image
            onClick={() => signOut()}
            className="rounded-full cursor-pointer hover:opacity-50"
            src={session.user?.image!}
            alt="User's profile picture"
            width={50}
            height={50}
          />
        </div>
      ) : (
        <div className="flex items-center justify-center text-red-900 font-extrabold">
          MED-45 AI
        </div>
      )}
    </div>
  );
}

export default Sidebar;
