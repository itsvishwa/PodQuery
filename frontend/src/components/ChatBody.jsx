import React, { useState } from "react";
import Question from "./Question";
import Answer from "./Answer";
import Thinking from "./Thinking";
import Welcome from "./Welcome";
import BottomPanel from "./BottomPanel";
import axios from "axios";

function ChatBody() {
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState("");
  // const [currentAnswer, setCurrentAnswer] = useState("");

  // send button handler
  const sentButtonHandler = (userInput) => {
    setLoading(true);
    setCurrentQuestion(userInput);
    console.log(userInput);

    axios
      .post("http://127.0.0.1:5000/question", {
        question: userInput,
      })
      .then((res) => {
        console.log(res.data);
        setChatHistory((prev) => [
          ...prev,
          {
            q: userInput,
            a: res.data.response,
          },
        ]);
        setCurrentQuestion("");
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setCurrentQuestion("");
        setLoading(false);
      });
  };

  return (
    <>
      <div className="h-[400px]">
        <div className="overflow-y-auto h-full scrollbar-thin scrollbar-thumb-[#023C92] scrollbar-track-[#babdc2] ">
          {/* initial state */}
          {currentQuestion === "" && chatHistory.length === 0 && <Welcome />}

          {/* Showing chat history */}
          {chatHistory.map((chat, index) => (
            <>
              <Question key={index + chat.q.slice(0, 5)} question={chat.q} />
              <Answer key={index + chat.a.slice(0, 5)} answer={chat.a} />
            </>
          ))}

          {/* Showing current question */}
          {currentQuestion !== "" && <Question question={currentQuestion} />}

          {/* Showing loading */}
          {loading && <Thinking />}
        </div>
      </div>
      <BottomPanel sentButtonHandler={sentButtonHandler} />
    </>
  );
}

export default ChatBody;
