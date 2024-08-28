import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import { SessionProvider } from "@/components/SessionProvider";
import { getServerSession } from "next-auth";
import { authOptions } from "@/pages/api/auth/[...nextauth]";
import Login from "@/components/Login";
import { useSession } from "next-auth/react";
import { SessionCheck } from "@/components/SessionCheck";
import ToastProvider from "@/components/ToastProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // const session = await getServerSession(authOptions); // Comment this out or remove it

  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider>
          <div className="flex">
            {/* header */}
            {/* sidebar */}
            <div className="max-w-xs h-screen overflow-y-auto md:min-w-[20rem]">
              <Sidebar />
            </div>
            {/* ToastProvider Notification */}
            <ToastProvider />
            <div className="flex-1 bg-gradient-to-bl from-white to-red-500">
              <SessionCheck>{children}</SessionCheck>
            </div>
          </div>
        </SessionProvider>
      </body>
    </html>
  );
}
