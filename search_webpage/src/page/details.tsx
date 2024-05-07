import React, {  useEffect, useState } from 'react';
import { Row, Col, Card, Button, Typography } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import '../css/productDetail.css'; 
import { axiosClient } from '../libraries/axiosClient';

const { Title, Paragraph } = Typography;
interface Product {
  sku: string;
  webName: string;
  image: string;
  specification: string;
  price: [string, string]; 
  currencySymbol: string;
  measureUnitName: [string, string]; 
  brand?: string;
}
  
const ProductDetail: React.FC = () => {
// Lấy tham số truy vấn từ URL
const productId = window.location.pathname.split('/').pop();
const [product, setProduct] = useState<[]>([]);

function truncateText(text: string, maxLength: number) {
  if (!text) return '...';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}
const getProduct = async () => {
    try {
        const response = await axiosClient.get(`/products/${productId}`);
         setProduct(response.data);
         console.log(response.data);
         console.log(productId);
         
    } catch (error) {
        console.error('Error:', error);
    }
}

useEffect(() => {
  getProduct();
}, []);


  return (
    <div className="product-detail-container">
     
      <Row justify="center" className="header">
        <Col span={20}>
          <Button type="text"  icon={<ArrowLeftOutlined />} onClick={() => window.history.back()} style={{ background: 'lightblue', margin: 10}}>
            Trang sản phẩm
          </Button>
          
        </Col>
       
      </Row>
      <Row justify="center" className="content">
        
        <Col span={20}>
        <h1 style={{textAlign: 'center', margin: '30px 0', color: 'red'}}>Chi tiết sản phẩm</h1>
        {product.map((product: any) => (
          <Card>
            <Row gutter={[24, 24]}>
              {/* Product Image */}
              <Col xs={24} sm={24} md={8}>
                <div className="product-image-container">
                  <img src={product.image} alt={product.webName} className="product-image" />
                </div>
              </Col>

              {/* Product Details */}
              <Col xs={24} sm={24} md={16}>
                <div className="product-details">
                  {/* Product Name */}
                  <Title level={1}>Sản phẩm: {truncateText(product.webName, 22)}</Title>
                  {/* Brand */}
                  <Title level={2}>Nhãn hàng: {product.brand}</Title>
                  
                  {/* Specification */}
                  <Paragraph>{product.specification}</Paragraph>
                  
                  
                  {/* Price */}
                  <Paragraph>
                    Price: {product.price[0]} {product.currencySymbol} / {product.measureUnitName[0]}
                  </Paragraph>
                  
                  {/* Add to Cart Button */}
                  <Button type="primary" size="large">Thêm vào giỏ hàng</Button>
                </div>
              </Col>
            </Row>
          </Card>
        ))}
        </Col>
      </Row>
    </div>
  );
};

export default ProductDetail;
