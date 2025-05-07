import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
//import './index.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Mainpage from './mainpage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
   <BrowserRouter>
    <Routes>
        <Route path="/" element={<Mainpage/>}/>
    </Routes>
   </BrowserRouter>
  </StrictMode>,
)
