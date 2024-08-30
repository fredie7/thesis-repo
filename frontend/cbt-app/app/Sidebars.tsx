"use client";

import { useSelector } from "react-redux";

function Sidebars({ children }: { children: React.ReactNode }) {
  const sidebarVisible = useSelector(
    (state: any) => state.toggle.sidebarVisible
  );
  console.log("sidebarVisible===>>s", sidebarVisible);
  return (
    <>
      {!sidebarVisible && (
        <div className="hidden md:flex max-w-xs h-screen overflow-y-auto md:min-w-[20rem]">
          {children}
        </div>
      )}
    </>
  );
}

export default Sidebars;
