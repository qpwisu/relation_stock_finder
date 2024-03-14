import { useState, useEffect } from 'react';


const host = process.env.REACT_APP_HOST
const port = process.env.REACT_APP_PORT

// 데이터를 가져오는 커스텀 훅
const useFetchPoliticianTotalData = (category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/total/category?category=${category}&period=${period}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [category,period]);
  return data; // 데이터 반환
};

const useFetchStockTotalData = (category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/total/stock?category=${category}&period=${period}`)
      .then(response => response.json())
      .then(data => {

        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [category,period]);
  return data; // 데이터 반환
};

const useFetchAggregateCategoryData = (company_name,category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/aggregate/category?company_name=${company_name}&category=${category}&period=${period}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [company_name,category,period]);
  return data; // 데이터 반환
};

const useFetchAggregateStockData = (name,category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/aggregate/stock?name=${name}&category=${category}&period=${period}`)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [name,category,period]);
  return data; // 데이터 반환
};


const useFetchBlog = (name,category,page) => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/blog?name=${name}&category=${category}&page=${page}`)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [name,category,page]);
  return data; // 데이터 반환
};

const useFetchDateAggregateStockData = (name,category) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/aggregate/date/category?name=${name}&category=${category}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [name,category]);
  return data; // 데이터 반환
};

const useFetchStockPriceData = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://${host}:${port}/api/stock/total/price`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  },[]); // 의존성 배열이 빈 배열이면, 컴포넌트 마운트 시 한 번만 호출됩니다.
  return data; // 데이터 반환
};

const useStockInfo = (company_name) => {
  const [stockInfo, setStockInfo] = useState(null);

  useEffect(() => {
      if (!company_name) return; // company_name이 없는 경우 early return

      const fetchStockInfo = async () => {
          try {
              const response = await fetch(`http://${host}:${port}/api/stock/info?company_name=${encodeURIComponent(company_name)}`);
              const data = await response.json();
              if (data.success) {
                  setStockInfo(data.data);
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockInfo();
  }, [company_name]);

  return stockInfo;
};

const useStockPrice = (company_name) => {
  const [stockPrice, setStockPrice] = useState(null);

  useEffect(() => {
      if (!company_name) return; // company_name이 없는 경우 early return

      const fetchStockPrice = async () => {
          try {
              const response = await fetch(`http://${host}:${port}/api/stock/price?company_name=${encodeURIComponent(company_name)}`);
              const data = await response.json();
              if (data.success) {
                setStockPrice(data.data);
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockPrice();
  }, [company_name]);

  return stockPrice;
};

const usePeriodStockPrice = (company_name) => {
  const [stockPrice, setStockPrice] = useState(null);

  useEffect(() => {
      if (!company_name) return; // company_name이 없는 경우 early return

      const fetchStockPrice = async () => {
          try {
              const response = await fetch(`http://${host}:${port}/api/stock/price/period?company_name=${encodeURIComponent(company_name)}`);
              const data = await response.json();
              if (data.success) {
                setStockPrice(data.data.reverse());
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockPrice();
  }, [company_name]);

  return stockPrice;
};

function highlightSearchTerm(text, searchTerm) {
  const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
  return (
      <span>
          {parts.map((part, index) =>
              part.toLowerCase() === searchTerm.toLowerCase() ? (
                  <span key={index} style={{ color: 'red' }}>{part}</span>
              ) : (
                  part
              )
          )}
      </span>
  );
}
export {highlightSearchTerm,useFetchBlog,useFetchDateAggregateStockData,useFetchAggregateCategoryData,useFetchAggregateStockData, usePeriodStockPrice,useStockPrice,useFetchPoliticianTotalData, useFetchStockTotalData,useFetchStockPriceData ,useStockInfo};

// export default useFetchStockData;