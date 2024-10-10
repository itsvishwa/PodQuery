import React from "react";
import welcomeImg from "./../assets/welcome.png";

function Welcome() {
  return (
    <div className="text-center text-black p-4 flex flex-col justify-center h-full">
      <div className="flex justify-center w-full">
        <img
          src={welcomeImg}
          alt=""
          className="object-contain mix-blend-multiply w-60 "
        />
      </div>
      <h2 className="text-xl font-semibold">Welcome to PodQuery!</h2>
      <p className="mt-2">
        I'm here to assist you with any queries you have based on podcasts.
        <br />
        You can ask me questions about topics discussed, summaries, or even
        specific moments in a podcast episode.
      </p>
      <p className="mt-4">Type your first question to get started!</p>
    </div>
  );
}

export default Welcome;
