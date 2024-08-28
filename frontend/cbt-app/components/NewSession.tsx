"use client";
import { db } from "@/firebase";
import { addDoc, collection, serverTimestamp } from "firebase/firestore";
import { PlusIcon } from "lucide-react";
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
      className="flex border-gray-700 border btnStyle"
      onClick={createNewSession}
    >
      <PlusIcon className="h-4 w-4" />
      <p>New Therapy</p>
    </div>
  );
}

export default NewSession;
