import { BrowserRouter, Route, Routes } from 'react-router-dom'
import React from 'react';

import Homepage from './pages/Homepage';
import Registration from './pages/Registration';
import Login from './pages/Login';
import Welcome from './pages/Welcome'

function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Welcome/>} />
          <Route exact path="/home" element={<Homepage/>} />
          <Route exact path="/registration" element={<Registration/>}/>
          <Route exact path="/login" element={<Login/>}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;