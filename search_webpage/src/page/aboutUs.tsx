import React from 'react';
import { Card, Row, Col, Typography } from 'antd';
const { Title, Text } = Typography;


const AboutUs: React.FC = () => {

    const Student = [
    { 
      urlImage:  require('../images/Minh.jpg'),
      name: 'Phan Lê Văn Minh',
      studentId: '21115053120356'
    },
    { 
        urlImage: require('../images/duc.jpg'),
        name: 'Lê Phước Đức',
        studentId: '21115053120310'
      },
      { 
        urlImage: require('../images/lam.jpg'),
        name: 'Trương Văn Lâm',
        studentId: '21115053120326'
      },
      { 
        urlImage: require('../images/phu.jpg'),
        name: 'Trần Công Quang Phú',
        studentId: '21115053120339'
      },
      { 
        urlImage: require('../images/Truc.jpg'),
        name: 'Phạm Thanh Trúc',
        studentId: '21115053120356'
      },]
  return (
    <>
    <Title level={1} style={{textAlign: 'center', margin: "40px 0"}}>Nhóm Đẹp Trai Nhất VN</Title>
    <Row gutter={[16, 16]} justify="center" >
        
    {Student.map((student: any, index) => (
      <Col key={index} xs={24} sm={12} md={8} lg={4}>
        <Card
        
        >
          <img alt="Student Avatar" src={student.urlImage} style={{ width: '100%', height: 'auto' }} />
          <div style={{ marginTop: 16, alignItems: 'center' }}>
           
            <Title level={4}>Họ và tên</Title>
            <Text>{student.name}</Text>
            
            <Title level={4} style={{ marginTop: 16 }}>Mã sinh viên</Title>
            <Text>{student.studentId}</Text>
            
          </div>
        </Card>
      </Col>
    ))}
  </Row>
  </>
  );
};

export default AboutUs;