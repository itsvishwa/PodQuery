import React from "react";
import { RiRobot3Fill } from "react-icons/ri";
import Lottie from "lottie-react";
import loadingAnimation from "./../assets/animation.json";
import botImg from "./../assets/bot.png";

function Thinking() {
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
      <div className="flex-1 pl-20">
        <Lottie
          animationData={loadingAnimation}
          style={{ width: 40, height: 40 }}
        />
      </div>
    </div>
  );
}

export default Thinking;
