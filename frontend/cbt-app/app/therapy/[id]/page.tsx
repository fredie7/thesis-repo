"use client";
import React, { FormEvent, useEffect, useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatSession from "@/components/ChatSession";
import { SendHorizonal } from "lucide-react";
import { useSession } from "next-auth/react";
import Image, { StaticImageData } from "next/image";
import img1 from "../../../images/img2.jpeg";
import img3 from "../../../images/img3.jpeg";
import {
  addDoc,
  collection,
  doc,
  onSnapshot,
  orderBy,
  query,
  updateDoc,
} from "firebase/firestore";
import { db } from "@/firebase";
import ThreeDots from "react-loading-icons/dist/esm/components/three-dots";
import Header from "@/components/Header";

type Props = {
  params: {
    id: string;
  };
};

interface ChatEntry {
  question: string;
  answer: string | null;
}

interface UserProfileImageProps {
  src?: string | StaticImageData;
}

function Therapy({ params: { id } }: Props) {
  const { data: session } = useSession();
  const [prompt, setPrompt] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatEntry[]>([]);
  const [loading, setLoading] = useState(false);

  const UserProfileImage = ({ src }: UserProfileImageProps) => {
    return (
      <div className="relative h-12 w-12 rounded-full overflow-hidden border border-gray-300">
        {src ? (
          <Image src={src} alt="User Profile" layout="fill" objectFit="cover" />
        ) : (
          <Image
            src="/default-profile.png"
            alt="Default Profile"
            layout="fill"
            objectFit="cover"
          />
        )}
      </div>
    );
  };

  async function handleChat(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const currentQuestion = question;
    console.log("currentQuestion===>>", question);

    // Clear the input field immediately
    setQuestion("");

    setLoading(true); // Start loading

    let docRef; // Declare docRef here to make it accessible in the catch block

    try {
      // Store the question in Firestore with a placeholder for the answer
      docRef = await addDoc(
        collection(db, "users", session?.user?.email!, "chats", id, "messages"),
        {
          question: currentQuestion,
          answer: null, // Answer is initially null
          timestamp: new Date(),
        }
      );

      // Fetch the answer from your backend
      // const response = await fetch("http://127.0.0.1:8000/ask", {
      const response = await fetch("http://100.27.241.218:80/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: currentQuestion }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("DATA=====>>", data.response);
      const newAnswer = data.response;

      // Update the existing document in Firestore with the answer
      await updateDoc(
        doc(
          db,
          "users",
          session?.user?.email!,
          "chats",
          id,
          "messages",
          docRef.id
        ),
        {
          answer: newAnswer,
          timestamp: new Date(),
        }
      );
    } catch (error) {
      console.error("Error fetching data:", error);

      // Handle error by updating the document with an error message
      if (docRef) {
        await updateDoc(
          doc(
            db,
            "users",
            session?.user?.email!,
            "chats",
            id,
            "messages",
            docRef.id
          ),
          {
            answer: "There was an error processing your request.",
            timestamp: new Date(),
          }
        );
      }
    } finally {
      setLoading(false); // Stop loading
    }
  }
  console.log("CHATHISTORY DATA===>>>", chatHistory);
  const sessionEmail = session && session?.user?.email;
  useEffect(() => {
    const q = query(
      collection(db, "users", session?.user?.email!, "chats", id, "messages"),
      orderBy("timestamp", "asc")
    );

    const unsubscribe = onSnapshot(q, (querySnapshot) => {
      const messages: ChatEntry[] = [];
      querySnapshot.forEach((doc) => {
        messages.push(doc.data() as ChatEntry);
      });
      setChatHistory(messages);
    });

    // Cleanup the listener on unmount
    return () => unsubscribe();
  }, [session?.user?.email, id]); // Include 'id' here

  return (
    <>
      <div className="flex flex-col h-screen overflow-hidden">
        <Header />
        <div className="flex-1 overflow-auto p-2">
          {chatHistory.length === 0 ? (
            <>
              <p className="text-center">
                Ask me anything concerning your Mental Health Challenge
              </p>
            </>
          ) : (
            chatHistory.map((item, index) => (
              <div key={index}>
                <div className="flex justify-end space-x-3 mt-6">
                  <div className="flex-shrink-0">
                    <UserProfileImage src={session?.user?.image ?? ""} />
                  </div>
                  <div className="bg-stone-500 text-white p-3 rounded-lg max-w-xs shadow">
                    {item.question}
                  </div>
                </div>
                {/* AI's Message */}
                {item.answer !== null && (
                  <div className="flex justify-start space-x-3 mt-4">
                    <div className="flex-shrink-0 mt-6">
                      <UserProfileImage src={img3} />
                    </div>
                    <div className="bg-gray-300 text-black p-3 rounded-lg max-w-xs shadow border">
                      {item.answer}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <p className="text-center text-blue-500">
              <ThreeDots />
            </p>
          )}
        </div>

        <div className="bg-white text-black text-sm">
          <form className="p-5 space-x-5 flex" onSubmit={handleChat}>
            <input
              className="bg-transparent focus:outline-none flex-1 disabled:cursor-not-allowed disabled:text-gray-300 disabled:{!session}"
              type="text"
              onChange={(e) => setQuestion(e.target.value)}
              value={question}
              placeholder="Type your message here..."
            />
            <button
              type="submit"
              disabled={!session || !question}
              className="bg-red-900 hover:opacity-50 text-white font-bold px-4 py-2 rounded disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              <SendHorizonal className="h-4 w-4 -rotate-45" />
            </button>
          </form>
        </div>
      </div>
    </>
  );
}

export default Therapy;
