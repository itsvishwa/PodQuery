import React, { useState } from "react";
import { BsFillSendFill } from "react-icons/bs";

function BottomPanel({ sentButtonHandler }) {
  const [userInput, setUserInput] = useState("");

  return (
    <div className="bg-[#babdc2] p-4 rounded-b-md">
      <div className="bg-[#e0e2e7] rounded-md p-2">
        <textarea
          className="text-[#000] w-full bg-transparent focus:outline-none resize-none px-2"
          placeholder="Enter your question"
          rows="3"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        ></textarea>
        <div className="flex flex-row justify-end mt-2">
          <div
            onClick={() => {
              if (!userInput) return;
              sentButtonHandler(userInput);
              setUserInput("");
            }}
            className={
              userInput
                ? "bg-[#1c6de7] hover:cursor-pointer hover:bg-[#033c92] text-white px-4 py-2 rounded-md"
                : "bg-[#9ca8b9] text-[#697585] px-4 py-2 rounded-md"
            }
          >
            <BsFillSendFill />
          </div>
        </div>
      </div>
    </div>
  );
}

export default BottomPanel;
