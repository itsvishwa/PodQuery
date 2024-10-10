import MainBody from "./components/MainBody";
import { AuroraBackground } from "./components/ui/aurora-background";

export default function App() {
  return (
    <AuroraBackground>
      <div className="bg-[#1a1f25] w-full h-screen flex flex-col justify-center items-center">
        <MainBody />
      </div>
    </AuroraBackground>
  );
}
