import React from "react";
import { FaUserCircle } from "react-icons/fa";

function Question({ question }) {
  return (
    <div className="flex flex-col items-start py-4">
      <div className="flex items-center">
        <div className="w-20 flex justify-center text-2xl text-[#033c92]">
          <FaUserCircle />
        </div>
        <p className="text-[#000000] text-sm">You</p>
      </div>
      <div className="flex-1  pl-20">
        <p className="text-[#000]">{question}</p>
      </div>
    </div>
  );
}

export default Question;
