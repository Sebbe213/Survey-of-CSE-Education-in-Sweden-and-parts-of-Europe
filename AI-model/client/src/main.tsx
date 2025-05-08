import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
//import './index.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Mainpage from './mainpage.tsx'
import About from './about.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
   <BrowserRouter>
    <Routes>
        <Route path="/" element={<Mainpage/>}/>
        <Route path="/about" element={<About/>}/>
    </Routes>
   </BrowserRouter>
  </StrictMode>,
)
