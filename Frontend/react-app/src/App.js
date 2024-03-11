import './App.css';

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FirstPage from './pages/FirstPage'; // 여기서 FirstPage 컴포넌트를 임포트합니다.
import PoliticianPage from './pages/PoliticianPage';
import StockPage from './pages/StockPage';
import SectorPage from './pages/SectorPage';
import ThemaPage from './pages/ThemaPage';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FirstPage />} /> {/* FirstPage를 기본 페이지로 설정 */}
        <Route path="/stock" element={<StockPage />} /> {/* FirstPage를 기본 페이지로 설정 */}
        <Route path="/politician" element={<PoliticianPage />} /> {/* FirstPage를 기본 페이지로 설정 */}
        <Route path="/sector" element={<SectorPage />} /> {/* FirstPage를 기본 페이지로 설정 */}
        <Route path="/thema" element={<ThemaPage />} /> {/* FirstPage를 기본 페이지로 설정 */}

        {/* 여기에 추가 라우트를 설정할 수 있습니다. */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;