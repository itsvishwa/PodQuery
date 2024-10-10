import React from "react";
import ChatBody from "./ChatBody";
import BottomPanel from "./BottomPanel";

function MainBody() {
  return (
    <div
      className="flex flex-col justify-between bg-[#cacfd6] w-3/4 h-4/5 rounded-md shadow-lg z-[9999] relative"
      style={{ zIndex: 9999 }}
    >
      <div className="text-black rounded-tl-md rounded-tr-md bg-[#cacfd6] flex justify-center py-2">
        <p className="font-myTitle text-2xl font-bold">PodQuery</p>
      </div>
      <div className="flex-1">
        <ChatBody />
      </div>
    </div>
  );
}

export default MainBody;
