import './App.css';
import React, {useEffect} from "react";
import HomePage from "./components/pages/home/HomePage";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import StatsPage from "./components/pages/stats/StatsPage";
import {Simulate} from "react-dom/test-utils";
import change = Simulate.change;

function App() {
    function changeGradientOnMouseMove(event: MouseEvent) {
        setTimeout(() => {
            document.body.style.background = `radial-gradient(at ${event.clientX}px ${event.clientY}px, #ff3ea1, #4247f8, #313131)`;
        }, 100);
    }

    useEffect(() => {
        document.addEventListener("mousemove", changeGradientOnMouseMove);

        return () => {
          document.removeEventListener("mousemove", changeGradientOnMouseMove);
        };
    }, []);

  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stats/:key" element={<StatsPage />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;
