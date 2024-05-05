import React from 'react';
import { Layout, Row, Col } from 'antd';
import footer from '../images/footer.jpg';

const { Footer } = Layout;
window.addEventListener('scroll', () => {
  const footer = document.querySelector('.ant-layout-footer') as HTMLElement;
  const scrollPosition = window.scrollY;
  const windowHeight = window.innerHeight;
  const bodyHeight = document.body.offsetHeight;

  // Kiểm tra xem vị trí cuộn của trang có ở cuối cùng hay không
  if (scrollPosition + windowHeight >= bodyHeight) {
      footer.style.display = 'none'; // Ẩn footer khi cuộn xuống cuối trang
  } else {
      footer.style.display = 'block'; // Hiện footer trong các trường hợp khác
  }
});


const CustomFooter: React.FC = () => {
  return (
    <Footer style={{ backgroundColor: '#f0f2f5', padding: '24px 50px', position: 'fixed', bottom: 0, width: '100%' }}>
      <Row justify="space-between" align="middle">
        <Col flex="auto">
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <img src={footer} alt="Logo" style={{ width: '80px', marginRight: '16px' }} />
            <span style={{ fontSize: '18px', fontWeight: 'bold' }}>Footer</span>
          </div>
        </Col>
        <Col flex="auto">
          <Row gutter={[16, 16]} justify="end">
            <Col>
              <div style={{ fontSize: '16px', color: '#333' }}>Về chúng tôi</div>
            </Col>
            <Col>
              <div style={{ fontSize: '16px', color: '#333' }}>Danh mục</div>
            </Col>
            <Col>
              <div style={{ fontSize: '16px', color: '#333' }}>Tìm hiểu thêm</div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Footer>
  );
};

export default CustomFooter;
