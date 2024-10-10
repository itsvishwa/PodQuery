import React from "react";
import botImg from "./../assets/bot.png";

function Answer({ answer }) {
  return (
    <div className="flex flex-col items-start py-4 bg-[#dbdbdb]">
      <div className="flex items-center">
        <div className="w-20 flex justify-center text-2xl">
          <div className="avatar">
            <div className="w-8">
              <img src={botImg} alt="Tailwind-CSS-Avatar-component" />
            </div>
          </div>
        </div>
        <p className="text-[#000] text-sm">PodQuery</p>
      </div>
      <div className="flex-1 px-20">
        <p className="text-[#000]">{answer}</p>
      </div>
    </div>
  );
}

export default Answer;
