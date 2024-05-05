import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './page/home';
import HeaderLayout from './page/header';
import CustomFooter from './page/footer';
import CustomContent from './page/content';
import LoginForm from './page/login';
import ProductDetail from './page/details';


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
     <BrowserRouter>
    <HeaderLayout/>
     <Routes>
       <Route path='/' element={<App/>}/>
         <Route path='/Home' element={<Home/>}/>
         <Route path='/products' element={<CustomContent  />}/>
       
         <Route/>
         <Route path='/login' element={<LoginForm  />}/>
         <Route path='/products/:sku' element={<ProductDetail  />}/>
         
         <Route/>
      <Route/>
  </Routes>
  <CustomFooter/>
  
    </BrowserRouter>
  </React.StrictMode>
  
);





// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();