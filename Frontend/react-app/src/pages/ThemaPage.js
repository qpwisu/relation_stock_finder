import '../App.css';
import React, { useEffect, useState,useRef } from 'react';
import {Button, Typography ,Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Select, MenuItem, FormControl, InputLabel,Grid } from '@mui/material';
import {highlightSearchTerm,useFetchBlog, useFetchAggregateStockData,useFetchDateAggregateStockData} from '../useFetchData';
import { createChart } from 'lightweight-charts';
import Layout from '../Layout';
import { useLocation,useNavigate } from 'react-router-dom';

function ThemaPage() {
    const navigate = useNavigate(); // useNavigate 훅을 사용
    const handleNameClick = (category,Name) => {
      switch(category){
        case 'thema':
          navigate('/thema', { state: { searchTerm: Name } });
          break;
      case 'politician':
          navigate('/politician', { state: { searchTerm: Name } });
          break;
      case 'stock':
          navigate('/stock', { state: { searchTerm: Name } });
          break;
      case 'sector':
          navigate('/sector', { state: { searchTerm: Name } });
          break;
      default:
          console.log('Unknown search type');
      }
    };

    const location = useLocation();
    const searchTerm = location.state?.searchTerm;
    const data = useFetchDateAggregateStockData(searchTerm,"thema"); 

    const [currentPage, setCurrentPage] = useState(1); // 현재 페이지 번호
    let posts = useFetchBlog(searchTerm,"thema",currentPage)

    let thema_data = data.map(item => ({
        time: item.date,
        value: item.cnt,
    }));    

    const chartContainerRef = useRef(null); // 차트를 그릴 컨테이너의 ref
    const chartRef = useRef(null); // 차트 인스턴스를 저장하는 ref

    const [period, setPeriod] = useState(30);
    const data2 = useFetchAggregateStockData(searchTerm,"thema",period); 
    const handlePeriodChange = (event) => {
        setPeriod(event.target.value);
    };
    

    useEffect(() => {
        if (thema_data && Array.isArray(thema_data) && thema_data.length > 0 && chartContainerRef.current) {
                if (chartRef.current) {
                    chartContainerRef.current.innerHTML = '';
                }
            
            const chart = createChart(chartContainerRef.current, {
                width: chartContainerRef.current.offsetWidth,
                height: 300,
                layout: {
                    backgroundColor: '#ffffff',
                    textColor: 'rgba(33, 56, 77, 1)',
                },
                grid: {
                    vertLines: {
                        color: 'rgba(197, 203, 206, 0.7)',
                    },
                    horzLines: {
                        color: 'rgba(197, 203, 206, 0.7)',
                    },
                },
                timeScale: {
                    borderVisible: false,
                },
            });

            const lineSeries = chart.addLineSeries();   

            chart.timeScale().applyOptions({
                fixLeftEdge: true,
                fixRightEdge: true,
                rightOffset: 10,
                borderVisible: false,
            });
            const data = thema_data;

            lineSeries.setData(data);

            // 차트 크기를 반응형으로 조정
            const handleResize = () => {
                if (chartContainerRef.current!= null){
                    chart.applyOptions({ width: chartContainerRef.current.offsetWidth });
                }
            };
            window.addEventListener('resize', handleResize);
            chartRef.current = chart;

        }
    }, [thema_data]); // 의존성 배열을 빈 배열로 설정하여 컴포넌트 마운트 시에만 실행

    return (
        <Layout>
                <Grid container spacing={1} style={{ maxWidth: '1300px', margin: '0 auto', padding: '18px 20px 13px', backgroundColor: "#ffffff" }}>
                    <Grid item xs={12} md={12}>
                        <Typography variant="h6" component="h3" gutterBottom>
                            테마 : {searchTerm}
                        </Typography>
                        <div className="DividingLine_line__gjUrd"></div>

                    </Grid>
                    <Grid item style={{ width: '100%' }}>
                        <h2>날짜별 언급 추이</h2>
                        <div ref={chartContainerRef} style={{ width: '100%', height: '300px' }} />
                        <div className="DividingLine_line__gjUrd"></div>
                    </Grid>
                    <Grid item xs={12} md={12} style={{paddingLeft:0}}>
                        <h2 style={{marginTop:0}}>관련 종목 언급 순위</h2>
                        <FormControl fullWidth>
                            <InputLabel id="period-select-label">Period</InputLabel>
                            <Select
                            labelId="period-select-label"
                            id="period-select"
                            value={period}
                            label="Period"
                            onChange={handlePeriodChange}
                            >
                            <MenuItem value={1}>1</MenuItem>
                            <MenuItem value={7}>7</MenuItem>
                            <MenuItem value={30}>30</MenuItem>
                            <MenuItem value={90}>90</MenuItem>
                            <MenuItem value={180}>180</MenuItem>
                            </Select>
                        </FormControl>
                        <TableContainer component={Paper} className="childGrid">
                            <Table aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                <TableCell>Ranking</TableCell>
                                <TableCell>thema</TableCell>
                                <TableCell align="right">Count</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody  style={{minHeight:'585px'}}>
                                {data2.map((row) => (
                                <TableRow key={row.ranking}>
                                    <TableCell  component="th" scope="row">{row.ranking}</TableCell>
                                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("stock",row.company_name)}>{row.company_name}</TableCell>
                                    <TableCell align="right">{row.cnt}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                            </Table>
                        </TableContainer>
                        </Grid>
                        <div>
                            <div   style={{borderBottom: '2px solid #eee'}}>
                              <h1>블로그 포스트</h1>
                              {posts.map((post, index) => (
                                <div key={index} style={{borderTop: '2px solid #eee', cursor: 'pointer', padding: '10px'}}>
                                    <h3 onClick={() => window.location.href = post.href}>
                                        {highlightSearchTerm(post.title, searchTerm)}
                                    </h3>
                                    <p onClick={() => window.location.href = post.href}>
                                        {highlightSearchTerm(post.header, searchTerm)}
                                    </p>
                                    <p>{post.date}</p>
                                </div>
                            ))}
                            </div>

                            <div style={{display: 'flex', justifyContent: 'center', margin: '20px 0'}}>
                                <Button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1}>
                                    이전
                                </Button>
                                <Button onClick={() => setCurrentPage(currentPage + 1)} disabled={posts.length === 0}>
                                    다음
                                </Button>
                            </div>
                        </div>
                    
                </Grid>
        </Layout>
        )
}

export default ThemaPage;