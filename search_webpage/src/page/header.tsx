import React, { useEffect, useState } from 'react';
import { Layout, Menu, Input, Button, Badge } from 'antd';
import { ShoppingCartOutlined } from '@ant-design/icons';
import '../css/header.css';
import logo from '../images/logo.png';
import {  Link} from 'react-router-dom';
import { ProductOutlined, UsergroupAddOutlined} from '@ant-design/icons';
import Cookies from 'js-cookie';


const { Header } = Layout;
const HeaderLayout: React.FC = () => {
  const [loggedIn, setLoggedIn] = useState(false); 
  const [username, setUsername] = useState('string'); 

  useEffect(() => {
    // Kiểm tra cookie có lưu username không
    const username = Cookies.get('username');
    if (username) {
      setLoggedIn(true); // Đã đăng nhập
      setUsername(username);
      
    } else {
      setLoggedIn(false); // Chưa đăng nhập
    }
  }, []);

  const logOut = () => {
    Cookies.remove('username');
    setLoggedIn(false);
    window.location.href = '/login';
  }

  return (
    
    <Header className="header">
       
      <div className="logo" style={{ height: 64, display: 'inline-block' }}>
        <img src={logo} alt="Long Châu Logo" style={{ height: '100%' }} />
      </div>
      <Menu theme="light" mode="horizontal" defaultSelectedKeys={['home']} className="menu">
       
        <Menu.Item icon={<ProductOutlined />} key="products" ><Link to='/products'>Sản phẩm</Link></Menu.Item> 
        <Menu.Item icon={<UsergroupAddOutlined />}  key="about"><Link to='/aboutUs'>Giới thiệu</Link></Menu.Item>

       
      </Menu>
    
    {loggedIn ? (
      <div className="left-content">
        <Button type="primary" className="primary-button"> <Link to="/login"> {username} </Link></Button>
        <Button type="primary" className="register-button" onClick={logOut}>Đăng xuất</Button>
        <Badge count={5}>
          <Button type="primary" shape="circle" icon={<ShoppingCartOutlined />} />
        </Badge>
      </div>
    ) : (
      <div className="left-content">
        <Button type="primary" className="primary-button"> <Link to="/login">Đăng nhập</Link></Button>
        <Button type="primary" className="register-button"> <Link to="/register">Đăng ký</Link></Button>
        <Badge count={5}>
          <Button type="primary" shape="circle" icon={<ShoppingCartOutlined />} />
        </Badge>
      </div>
    )}
     
    </Header>
  )
};


export default HeaderLayout;
