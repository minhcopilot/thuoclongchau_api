import React, {  useState } from 'react';
import { Row, Col, Card, Button, Typography } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import '../css/productDetail.css'; 

const { Title, Paragraph } = Typography;
interface Product {
    sku: string;
    image: string;
    webName: string;
    price?: any;
    specification?: string;
    measureUnitName?: any;
    brand?: string;
   
  
  }
  
const ProductDetail: React.FC = () => {
// Lấy tham số truy vấn từ URL
const [product] = useState<Product>(
  {
    "sku": "00000500",
    "webName": "Trà tăng huyết áp Acotea QD-Meliphar hỗ trợ điều trị huyết áp thấp, tăng cường sinh lực (4g x 20 gói)",
    "image": "https://cdn.nhathuoclongchau.com.vn/unsafe/https://cms-prod.s3-sgn09.fptcloud.com/DSC_04158_261a268700.jpg",
    "specification": "Hộp 20 gói",
    "brand": "MERACINE",
    
    "price": [
        "2900",
        "58000"
    ],
    "measureUnitName": [
        "Gói",
        "Hộp"
    ]
}
);
 

// const getProduct = async () => {
//     try {
//         const response = await axiosClient.get(`/products/${productId}`);
//          setProduct(response.data);
//          console.log(response.data);
//          console.log(productId);
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// useEffect(() => {
//   getProduct();
// },[]);


  return (
    <div className="product-detail-container">
      <Row justify="center" className="header">
        <Col span={20}>
          <Button type="text" icon={<ArrowLeftOutlined />} onClick={() => window.history.back()}>
            Back
          </Button>
        </Col>
      </Row>
      <Row justify="center" className="content">
        <Col span={20}>
          <Card>
            <Row gutter={[24, 24]}>
              <Col xs={24} sm={24} md={10}>
                <img src={product?.image} alt={product?.webName} className="product-image" />
              </Col>
              <Col xs={24} sm={24} md={14}>
                <div className="product-details">
                  <Title level={2}>{product?.brand}</Title>
                  <Paragraph>{product?.specification}</Paragraph>
                  <Title level={3}>{product?.sku}</Title>
                  <Button type="primary" size="large">Add to Cart</Button>
                </div>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ProductDetail;
