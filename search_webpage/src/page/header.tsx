import React from 'react';
import { Layout, Menu, Input, Button, Badge } from 'antd';
import { ShoppingCartOutlined } from '@ant-design/icons';
import '../css/header.css';
import logo from '../images/logo.png';
import {  Link} from 'react-router-dom';


const { Header } = Layout;
const { Search } = Input;

const HeaderLayout: React.FC = () => {
  return (
    <Header className="header">
      <div className="logo" style={{ height: 64, display: 'inline-block' }}>
        <img src={logo} alt="Long Châu Logo" style={{ height: '100%' }} />
      </div>
      <Menu theme="light" mode="horizontal" defaultSelectedKeys={['home']} className="menu">
       
        <Menu.Item key="products"><Link to='/products'>Sản phẩm</Link></Menu.Item> 
        <Menu.Item key="about"><Link to='/aboutUs'>Giới thiệu</Link></Menu.Item>

       
      </Menu>
    
  
      <div className="left-content">
        <Button type="primary" className="primary-button"> <Link to="/login"> Đăng nhập </Link></Button>
        <Button type="primary" className="register-button">Đăng ký</Button>
        <Badge count={5}>
          <Button type="primary" shape="circle" icon={<ShoppingCartOutlined />} />
        </Badge>
      </div>
    </Header>
  );
};

export default HeaderLayout;
