import React, { useState } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { axiosClient } from '../libraries/axiosClient';

const RegisterPage: React.FC = () => {
  const [form] = Form.useForm();
  
  const onFinishRegister = async (values: any) => {
    const usernameRegister = values.username;
    const   passwordRegister = values.password;      
try {

    
     const response = await axiosClient.post(`/register`, { username: usernameRegister, password: passwordRegister });
     if (response.status === 200) {
      if (response.data.message === 'User registered successfully') {
        console.log('Đăng kí thành công');
        // Thông báo thành công đăng kí
      
        message.success('Đăng kí thành công');
        // Chuyển hướng người dùng đến trang chính sau khi đăng kí thành công
        window.location.href = '/login';
        
      } else {
        console.error('Đăng kí thất bại');
        // Hiển thị thông báo lỗi cho người dùng khi đăng nhập thất bại
        message.error('Đăng kí thất bại');
      }
     }
    } catch (error) {
      console.error('Error:', error);
      message.error('An error occurred while logging in');
    }
  };

  return (
    <>
    <h1 style={{textAlign: "center"}}>Đăng ký tài khoản</h1>
      <Form form={form} name="register" onFinish={onFinishRegister} 
      initialValues={{ remember: true }}
      style={{ maxWidth: 300, margin: 'auto', marginTop: 50 }}>
        <Form.Item
          name="username"
          rules={[{ required: true, message: 'Vui lòng nhập tên đăng nhập!' }]}
        >
          <Input prefix={<UserOutlined />} placeholder="Tên đăng nhập" />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
        >
          <Input.Password prefix={<LockOutlined />} placeholder="Mật khẩu" />
        </Form.Item>
        <Form.Item
          name="confirmPassword"
          dependencies={['password']}
          rules={[
            { required: true, message: 'Vui lòng xác nhận mật khẩu!' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error('Mật khẩu xác nhận không trùng khớp!'));
              },
            }),
          ]}
        >
          <Input.Password prefix={<LockOutlined />} placeholder="Xác nhận mật khẩu" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" style={{ width: '100%' }}  >
            Đăng ký
          </Button>
        </Form.Item>
      </Form>
      </>
   
  );
};

export default RegisterPage;
