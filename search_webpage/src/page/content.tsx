import React, { useEffect, useState } from 'react';
import { Layout, Input, Pagination, Button, Row, Col } from 'antd';
import { axiosClient } from '../libraries/axiosClient';
import { ProductOutlined } from '@ant-design/icons';
import '../css/content.css';

import { Link } from 'react-router-dom';
import { Script } from 'vm';
const { Content } = Layout;
const { Search } = Input;


interface Product {
  sku: number;
  image: string;
  webName: string;
  price?: [number];
  currencySymbol: string;
  measureUnitName: [string, string];

}

const CustomContent: React.FC = () => {

  const [searchProducts, setSearchProducts] = useState<Product[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [perPage] = useState<number>(24); // Số lượng sản phẩm trên mỗi trang
  const [products, setProducts] = useState<Product[]>([]);


  const getProducts = async () => {
    try {
      const response = await axiosClient.get('/products');
      setProducts(response.data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const getSearchProducts = async (keyword: string) => {
    try {
      const response = await axiosClient.get(`/search?s=${keyword}`);
      setSearchProducts(response.data);
   
    } catch (error) {
      console.error('Error:', error);
      return null;
    }
  }

  useEffect(() => {
    getProducts();
    const intervalId = setInterval(() => {
      getProducts();
      console.log('Interval activated');
    }, 5000);
  
    return () => clearInterval(intervalId); // Xóa interval khi component unmount để tránh memory leak
  }, []);
  
  // Sử dụng useEffect để theo dõi thay đổi trong products và cập nhật danh sách searchProducts
  useEffect(() => {
    setSearchProducts(products);
  }, [products]);


  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1); // Reset trang về trang đầu tiên sau mỗi lần tìm kiếm
    getSearchProducts(value);
  };

  const handleGetAll = () => {
    setSearchTerm("");
    setCurrentPage(1); // Reset trang về trang đầu tiên sau mỗi lần tìm kiếm
    getSearchProducts("");
  };


  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const startIndex = (currentPage - 1) * perPage;
  const endIndex = startIndex + perPage;
  const currentProducts = searchProducts.slice(startIndex, endIndex);




  function truncateText(text: string, maxLength: number) {
    if (!text) return '...';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  }


  return (
    <Layout>
      <Content style={{ padding: '0 50px', marginTop: 24 }}>
        <Button type="text" icon={<ProductOutlined />} onClick={handleGetAll} style={{ background: 'lightblue', margin: 10 }}>
          Tất cả sản phẩm
        </Button>
        <div style={{ background: '#fff', padding: 24, minHeight: 280, borderRadius: 8, boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)' }}>
          <Search
            placeholder="Tìm kiếm sản phẩm"
            allowClear
            enterButton="Tìm kiếm"
            size="large"
            value={searchTerm}
            onChange={(e: any) => setSearchTerm(e.target.value)}
            onSearch={handleSearch}
          />

          <div style={{ marginTop: 16, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 60 }}>
            {products.map((product) => {
              // Kiểm tra xem sản phẩm có trong danh sách hiện tại không
              if (currentProducts.some((currentProduct) => currentProduct.sku === product.sku)) {
                return (
                  <Link to={`/products/${product.sku}`} key={product.sku}>
                    <div key={product.sku} className="custom-card">
                      <div className="custom-card__image-container">
                        <img
                          src={product.image}
                          alt="example"
                          className="custom-card__image"
                        />
                      </div>
                      <div className="custom-card__content">
                        <h3 className="custom-card__title">{truncateText(product.webName, 20)}</h3>
                        {product.price && (
                          <p className="custom-card__description">
                            Price: {product.price[0]} {product.currencySymbol} / {product.measureUnitName[0]}
                          </p>
                        )}
                        <Button type="primary">Xem chi tiết</Button>
                      </div>
                    </div>
                  </Link>
                );
              } else {
                return null; // Nếu sản phẩm không nằm trong danh sách hiện tại, trả về null để không render
              }
            })}
          </div>

          <div style={{ marginTop: 16, textAlign: 'center' }}>
            <Pagination
              current={currentPage}
              pageSize={perPage}
              total={searchTerm !== '' ? searchProducts.length : products.length}
              onChange={handlePageChange}
            />
          </div>
        </div>
      </Content>
    </Layout>
  );
};




export default CustomContent;
