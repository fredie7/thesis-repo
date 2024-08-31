"use client";
import { LogOut, Menu } from "lucide-react";
import { signOut } from "next-auth/react";
import Image, { StaticImageData } from "next/image";
import React from "react";
import { useSession } from "next-auth/react";
import { useSelector, useDispatch } from "react-redux";
import { toggleSidebar } from "@/redux/toggleSlice";

function Header() {
  const dispatch = useDispatch();
  const { data: session } = useSession();
  const handleMenuClick = () => {
    dispatch(toggleSidebar());
  };

  return (
    <div className="flex items-center justify-between p-4 bg-gray-200 border-b sticky top-0 z-20">
      {/* Menu icon visible only on mobile */}
      <div className="flex items-center">
        {/* <Menu onClick={handleMenuClick} /> */}
        <div className="flex items-center justify-center text-red-900 font-extrabold">
          MED-45 AI
        </div>
      </div>

      {/* Right side buttons */}
      <div className="flex items-center space-x-4">
        <button className="bg-yellow-500 text-white px-3 py-1 rounded">
          Premium Upgrade
        </button>
        {/* <UserProfileImage src={med1} /> */}
        {/* <p>image</p> */}
        <div className="mx-auto mb-2">
          {/* <Image
            onClick={() => signOut()}
            className="rounded-full cursor-pointer hover:opacity-50"
            src={session && session.user?.image!}
            alt="User's profile picture"
            width={50}
            height={50}
          /> */}
          <LogOut />
        </div>
      </div>
    </div>
  );
}

export default Header;
