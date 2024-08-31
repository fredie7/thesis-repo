"use client";
import { db } from "@/firebase";
import { addDoc, collection, serverTimestamp } from "firebase/firestore";
import { MessageCirclePlus, PlusIcon } from "lucide-react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import React from "react";

function NewSession() {
  const router = useRouter();
  const { data: session } = useSession();

  const createNewSession = async () => {
    const doc = await addDoc(
      collection(db, "users", session?.user?.email!, "chats"),
      {
        userId: session?.user?.email!,
        createdAt: serverTimestamp(),
      }
    );
    router.push(`/therapy/${doc.id}`);
  };
  return (
    <div
      className="flex border-gray-200 border btnStyle h-10 sm:h-6"
      onClick={createNewSession}
    >
      <PlusIcon className="hidden md:flex h-4 w-4" />
      {/* <p>New Therapy</p> */}
      <p className="block sm:hidden">
        <MessageCirclePlus />
      </p>{" "}
      {/* Visible on mobile */}
      <button disabled={!session} className="hidden sm:block">
        New Therapy
      </button>{" "}
      {/* Visible on medium and desktop */}
    </div>
  );
}

export default NewSession;
