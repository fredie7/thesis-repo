import { db } from "@/firebase";
import { collection, deleteDoc, doc } from "firebase/firestore";
import { MessageSquareDot, Trash2 } from "lucide-react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import { useCollection } from "react-firebase-hooks/firestore";

type Props = {
  id: string;
};

function SessionRow({ id }: Props) {
  const pathname = usePathname();
  const router = useRouter();
  const { data: session } = useSession();
  const [active, setActive] = useState(false);

  const [messages] = useCollection(
    collection(db, "users", session?.user?.email!, "chats", id, "messages")
  );

  useEffect(() => {
    if (!pathname) return;
    setActive(pathname.includes(id));
  }, [pathname]);

  const removeChat = async () => {
    await deleteDoc(doc(db, "users", session?.user?.email!, "chats", id));
    router.replace("/");
  };

  return (
    <Link
      href={`/therapy/${id}`}
      className={`flex chatRow justify-center ${
        active && "bg-gray-700/50"
      } mt-3 pt-2 pb-2 items-center`}
    >
      <MessageSquareDot className="h-5 w-5 " />

      <p className="flex-1 hidden md:inline-flex truncate">
        {/* {messages?.docs[messages?.docs.length - 1]?.data().text ||
          "New Messages"} */}
        {messages && messages.docs.length > 0
          ? messages.docs.map((msg) => {
              const data = msg.data(); // Use the `data()` method to get document data
              const answer = data?.answer || ""; // Safely access the `answer` field
              return answer.split(" ").slice(0, 3).join(" ");
            })
          : "New Chat"}
      </p>
      <Trash2
        onClick={removeChat}
        className="h-5 w-5 text-gray-900 hover:text-red-700"
      />
    </Link>
  );
}

export default SessionRow;
