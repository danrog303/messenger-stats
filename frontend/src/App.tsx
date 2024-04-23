import './App.css';
import React from "react";
import HomePage from "./components/pages/home/HomePage";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import StatsPage from "./components/pages/stats/StatsPage";

function App() {
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
