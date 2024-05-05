import React, { useState } from 'react';
import { Layout, Input, Pagination, Button } from 'antd';
import { axiosClient } from '../libraries/axiosClient';
import '../css/content.css';

import { Link } from 'react-router-dom';
const { Content } = Layout;
const { Search } = Input;


interface Product {
  sku: number;
  image: string;
  webName: string;
  price?: [number];

}

const CustomContent: React.FC = () => {
  const [originalProducts, setOriginalProducts] = useState<Product[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [perPage] = useState<number>(24); // Số lượng sản phẩm trên mỗi trang
  const [products, setProducts] = useState<Product[]>([]);



  const getProducts = async () => {
    try {
      const response = await axiosClient.get('/products');
      setOriginalProducts(response.data);
      setProducts(response.data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  React.useEffect(() => {
    getProducts();
  }, []);

  const handleSearch = (value: string) => {
    const filteredProducts = originalProducts.filter((product) =>
      product.webName.toLowerCase().includes(value.toLowerCase())
    );
    setProducts(filteredProducts);
    setCurrentPage(1); // Reset trang về trang đầu tiên sau mỗi lần tìm kiếm
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const startIndex = (currentPage - 1) * perPage;
  const endIndex = startIndex + perPage;
  const currentProducts = products.slice(startIndex, endIndex);


  function truncateText(text: string, maxLength: number) {
    if (!text) return '...';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  }
  

  return (
    <Layout>
      <Content style={{ padding: '0 50px', marginTop: 24 }}>
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
  {currentProducts.map((product) => (
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
              Price: {product.price}
            </p>
          )}
          <Button type="primary">Xem chi tiết</Button>
        </div>
      </div>
    </Link>
  ))}
</div>

          <div style={{ marginTop: 16, textAlign: 'center' }}>
            <Pagination
              current={currentPage}
              pageSize={perPage}
              total={products.length} // Tổng số sản phẩm
              onChange={handlePageChange}
            />
          </div>
        </div>
      </Content>
    </Layout>
  );
};




export default CustomContent;
