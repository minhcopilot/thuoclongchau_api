import React, { useState } from 'react';
import { Form, Input, Button, Checkbox, Modal, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { axiosClient } from '../libraries/axiosClient';
const LoginForm: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);

  const onFinish = async (values: any) => {
    const username = values.username;
    const   password = values.password;      
try {

    
     const response = await axiosClient.post(`/login`, { username: username, password: password });
     if (response.status === 200) {
      // Kiểm tra nội dung của phản hồi để xác định đăng nhập có thành công hay không
      if (response.data.message === 'Login successful') {
        console.log('Đăng nhập thành công');
        // Thông báo thành công đăng nhập
        message.success('Đăng nhập thành công');
        // Chuyển hướng người dùng đến trang chính sau khi đăng nhập thành công
        window.location.href = '/';
      } else {
        console.error('Đăng nhập thất bại');
        // Hiển thị thông báo lỗi cho người dùng khi đăng nhập thất bại
        message.error('Thất bại');
      }
    }
    } catch (error) {
      console.error('Error:', error);
      message.error('An error occurred while logging in');
    }
  };

  const onFinishRegister = async (values: any) => {
    const usernameRegister = values.usernameR;
    const   passwordRegister = values.passwordR;      
try {

    
     const response = await axiosClient.post(`/register`, { username: usernameRegister, password: passwordRegister });
     if (response.status === 200) {
      if (response.data.message === 'User registered successfully') {
        console.log('Đăng kí thành công');
        // Thông báo thành công đăng nhập
        message.success('Đăng kí thành công');
        // Chuyển hướng người dùng đến trang chính sau khi đăng nhập thành công
        setLoading(false);
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

    <h1 style={{ textAlign: 'center', marginTop: 50 }}>Đăng nhập</h1>
    <Form
    name="login"
    initialValues={{ remember: true }}
    onFinish={onFinish}
    style={{ maxWidth: 300, margin: 'auto' }}
  >
    <Form.Item
      name="username"
      rules={[{ required: true, message: 'Hãy nhập tài khoản!' }]}
    >
      <Input prefix={<UserOutlined />} placeholder="Tài khoản" />
    </Form.Item>
    <Form.Item
      name="password"
      rules={[{ required: true, message: 'Hãy nhập mật khẩu!' }]}
    >
      <Input.Password prefix={<LockOutlined />} placeholder="Mật khẩu" />
    </Form.Item>
    <Form.Item>
      <Form.Item name="remember" valuePropName="checked" noStyle>
        <Checkbox>Ghi nhớ đăng nhập</Checkbox>
      </Form.Item>

      <a href="/forgot-password" style={{ float: 'right' }}>
       Quên mật khẩu?
      </a>
    </Form.Item>

    <Form.Item>
      <Button type="primary" htmlType="submit" style={{ width: '100%' }}>
        Log in
      </Button>
      Hoặc <a href='#!'onClick={() => setLoading(true)}>Đăng kí ngay</a>
    </Form.Item>
  </Form>


  <Modal
  title="Đăng ký tài khoản"
  visible={loading}
  onCancel={() => setLoading(false)} // Do nothing when cancel
  footer={null}
  
>
  <Form form={form} name="register" onFinish={onFinishRegister}>
    <Form.Item
      name="usernameR"
      rules={[{ required: true, message: 'Vui lòng nhập tên đăng nhập!' }]}
    >
      <Input prefix={<UserOutlined />} placeholder="Tên đăng nhập" />
    </Form.Item>
    <Form.Item
      name="passwordR"
      rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
    >
      <Input
        prefix={<LockOutlined />}
        type="password"
        placeholder="Mật khẩu"
      />
    </Form.Item>
    <Form.Item
      name="confirmPasswordR"
      dependencies={['password']}
      rules={[
        { required: true, message: 'Vui lòng xác nhận mật khẩu!' },
        ({ getFieldValue }) => ({
          validator(_, value) {
            if (!value || getFieldValue('passwordR') === value) {
              return Promise.resolve();
            }
            return Promise.reject(
              new Error('Mật khẩu xác nhận không trùng khớp!')
            );
          },
        }),
      ]}
    >
      <Input
        prefix={<LockOutlined />}
        type="password"
        placeholder="Xác nhận mật khẩu"
      />
    </Form.Item>
    <Form.Item>
      <Button
        type="primary"
        htmlType="submit"
        style={{ width: '100%' }}
        onClick={() => onFinishRegister}
      >
        Đăng ký
      </Button>
    </Form.Item>
  </Form>
</Modal>

  </>
  );
};

export default LoginForm;