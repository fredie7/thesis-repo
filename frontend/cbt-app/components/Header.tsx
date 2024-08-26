import { Menu } from "lucide-react";
import Image, { StaticImageData } from "next/image";
import React from "react";

function Header() {
  return (
    <div className="flex items-center justify-between p-4 bg-gray-200 border-b sticky top-0 z-20">
      {/* Menu icon visible only on mobile */}
      <div className="flex items-center">
        <Menu />
      </div>

      {/* Right side buttons */}
      <div className="flex items-center space-x-4">
        <button className="bg-yellow-500 text-white px-3 py-1 rounded">
          Premium Upgrade
        </button>
        {/* <UserProfileImage src={med1} /> */}
        <p>image</p>
      </div>
    </div>
  );
}

export default Header;
