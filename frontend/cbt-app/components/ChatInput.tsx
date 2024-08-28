"use client";
import { SendHorizonal } from "lucide-react";
import { useSession } from "next-auth/react";
import React, { FormEvent, useState } from "react";
type Props = {
  chatId: string;
};
function ChatInput({ chatId }: Props) {
  const { data: session } = useSession();
  const [prompt, setPrompt] = useState("");
  const sendChat = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };
  return (
    <div className="bg-white text-black text-sm">
      <form className="p-5 space-x-5 flex" onSubmit={sendChat}>
        <input
          className="bg-transparent focus:outline-none flex-1 disabled:cursor-not-allowed disabled:text-gray-300 disabled:{!session}"
          type="text"
          onChange={(e) => setPrompt(e.target.value)}
          value={prompt}
          placeholder="Type your message here..."
        />
        <button
          type="submit"
          disabled={!session || !prompt}
          className="bg-red-900 hover:opacity-50 text-white font-bold px-4 py-2 rounded disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          <SendHorizonal className="h-4 w-4 -rotate-45" />
        </button>
      </form>
    </div>
  );
}

export default ChatInput;
