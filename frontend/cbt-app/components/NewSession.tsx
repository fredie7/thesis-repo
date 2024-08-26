import { PlusIcon } from "lucide-react";
import React from "react";

function NewSession() {
  return (
    <div className="flex border-gray-700 border btnStyle">
      <PlusIcon className="h-4 w-4" />
      <p>New Therapy</p>
    </div>
  );
}

export default NewSession;
