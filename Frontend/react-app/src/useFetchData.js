import { useState, useEffect } from 'react';

// 데이터를 가져오는 커스텀 훅
const useFetchPoliticianTotalData = (category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8081/api/stock/total/category?category=${category}&period=${period}`)
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
    fetch(`http://localhost:8081/api/stock/total/stock?category=${category}&period=${period}`)
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

const useFetchAggregateCategoryData = (companyName,category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8081/api/stock/aggregate/category?companyName=${companyName}&category=${category}&period=${period}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setData(data.data);
        }
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, [companyName,category,period]);
  return data; // 데이터 반환
};

const useFetchAggregateStockData = (name,category,period) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8081/api/stock/aggregate/stock?name=${name}&category=${category}&period=${period}`)
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
    fetch(`http://localhost:8081/api/stock/blog?name=${name}&category=${category}&page=${page}`)
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
    fetch(`http://localhost:8081/api/stock/aggregate/date/category?name=${name}&category=${category}`)
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
    fetch(`http://localhost:8081/api/stock/total/price`)
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

const useStockInfo = (companyName) => {
  const [stockInfo, setStockInfo] = useState(null);

  useEffect(() => {
      if (!companyName) return; // companyName이 없는 경우 early return

      const fetchStockInfo = async () => {
          try {
              const response = await fetch(`http://localhost:8081/api/stock/info?companyName=${encodeURIComponent(companyName)}`);
              const data = await response.json();
              if (data.success) {
                  setStockInfo(data.data);
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockInfo();
  }, [companyName]);

  return stockInfo;
};

const useStockPrice = (companyName) => {
  const [stockPrice, setStockPrice] = useState(null);

  useEffect(() => {
      if (!companyName) return; // companyName이 없는 경우 early return

      const fetchStockPrice = async () => {
          try {
              const response = await fetch(`http://localhost:8081/api/stock/price?companyName=${encodeURIComponent(companyName)}`);
              const data = await response.json();
              if (data.success) {
                setStockPrice(data.data);
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockPrice();
  }, [companyName]);

  return stockPrice;
};

const usePeriodStockPrice = (companyName) => {
  const [stockPrice, setStockPrice] = useState(null);

  useEffect(() => {
      if (!companyName) return; // companyName이 없는 경우 early return

      const fetchStockPrice = async () => {
          try {
              const response = await fetch(`http://localhost:8081/api/stock/price/period?companyName=${encodeURIComponent(companyName)}`);
              const data = await response.json();
              if (data.success) {
                setStockPrice(data.data.reverse());
              }
          } catch (error) {
              console.error('Error fetching stock info:', error);
          }
      };

      fetchStockPrice();
  }, [companyName]);

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