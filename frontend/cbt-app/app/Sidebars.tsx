"use client";

import { useSelector } from "react-redux";
import { useSession } from "next-auth/react";
import Sidebar from "@/components/Sidebar";
function Sidebars({ children }: { children: React.ReactNode }) {
  const sidebarVisible = useSelector(
    (state: any) => state.toggle.sidebarVisible
  );
  console.log("sidebarVisible===>>s", sidebarVisible);
  const { data: session } = useSession();
  // return (
  //   <>
  //     {!sidebarVisible && (
  //       <div className="hidden md:flex max-w-xs h-screen overflow-y-auto md:min-w-[20rem]">
  //         {children}
  //       </div>
  //     )}
  //   </>
  // );
  if (session) {
    return (
      <div className="max-w-xs h-screen overflow-y-auto md:min-w-[20rem]">
        <Sidebar />
      </div>
    );
  }
}

export default Sidebars;
