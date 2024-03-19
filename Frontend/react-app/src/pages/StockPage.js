import React, { useEffect, useState,useRef } from 'react';
import { useLocation,useNavigate } from 'react-router-dom';
import { createChart } from 'lightweight-charts';
import Layout from '../Layout';
import { Card, CardContent, Typography ,Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Select, MenuItem, FormControl, InputLabel,Box,Grid } from '@mui/material';
import { useFetchDateAggregateStockData,useFetchAggregateCategoryData,useStockInfo, useStockPrice, usePeriodStockPrice } from '../useFetchData';
import '../myCss.css';


function StockPage() {
    const location = useLocation();

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

    const searchTerm = location.state?.searchTerm;

    const stockInfo = useStockInfo(searchTerm); // 커스텀 훅 사용하여 주식 정보 가져오기
    const stockPrice = useStockPrice(searchTerm);
    const PeriodStockPrice = usePeriodStockPrice(searchTerm);
    const [period5, setPeriod5] = useState(7);
    const [period6, setPeriod6] = useState(7);
    const [period7, setPeriod7] = useState(7);
    const data5 = useFetchAggregateCategoryData(searchTerm,"politician",period5); 
    const data6= useFetchAggregateCategoryData(searchTerm,"thema",period6); 
    const data7 = useFetchAggregateCategoryData(searchTerm,"sector",period7); 
      // Period 변경을 핸들링하는 함수
    const data8 = useFetchDateAggregateStockData(searchTerm,"stock"); 

    let data9 = data8.map(item => ({
        time: item.date,
        value: item.cnt,
    }));    

    const handlePeriodChange5 = (event) => {
    setPeriod5(event.target.value);
    };

    const handlePeriodChange6= (event) => {
    setPeriod6(event.target.value);
    };

    // Period 변경을 핸들링하는 함수
    const handlePeriodChange7 = (event) => {
    setPeriod7(event.target.value);
    };

    // 가격 변동률에 따른 색상 설정
    const change_rateStyle = (change_rate) => ({
        color: change_rate >= 0 ? '#ff0000' : '#0000ff',
    });

    const chartContainerRef = useRef(null); // 차트를 그릴 컨테이너의 ref
    const chartRef = useRef(null); // 차트 인스턴스를 저장하는 ref
    const chartContainerRef2 = useRef(null); // 차트 컨테이너에 대한 참조 생성
    const chartRef2 = useRef(null); // 차트 인스턴스를 저장하는 ref

    useEffect(() => {
        if (PeriodStockPrice && Array.isArray(PeriodStockPrice) && PeriodStockPrice.length > 0 && chartContainerRef.current) {
            // 기존 차트 인스턴스가 있으면 차트 컨테이너를 비웁니다.
            if (chartRef.current) {
                chartContainerRef.current.innerHTML = '';
            }

            const chart = createChart(chartContainerRef.current, {
                width: chartContainerRef.current.offsetWidth,
                height: 400,
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
            });
            chart.timeScale().applyOptions({
                fixLeftEdge: true,
                fixRightEdge: true,
                rightOffset: 50,
                borderVisible: false,
            });
            const candleSeries = chart.addCandlestickSeries();
            const data = PeriodStockPrice.map(item => ({
                time: item.date,
                open: item.open,
                high: item.high,
                low: item.low,
                close: item.close,
            }));

            candleSeries.setData(data);
            candleSeries.applyOptions({
                priceScale: {
                    borderVisible: false,
                    autoScale: true,
                },
            });
            // 새로운 차트 인스턴스를 저장합니다.
            chartRef.current = chart;
        }
    }, [PeriodStockPrice]);




    useEffect(() => {
        if (data9 && Array.isArray(data9) && data9.length > 0 && chartContainerRef2.current) {
                if (chartRef2.current) {
                    chartContainerRef2.current.innerHTML = '';
                }
            
            const chart = createChart(chartContainerRef2.current, {
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
            const data = data9;

            lineSeries.setData(data);

            // 차트 크기를 반응형으로 조정
            const handleResize = () => {
                if (chartContainerRef.current!= null){
                    chart.applyOptions({ width: chartContainerRef.current.offsetWidth });
                }
            };

            window.addEventListener('resize', handleResize);
            chartRef2.current = chart;

        }
    }, [data9]); // 의존성 배열을 빈 배열로 설정하여 컴포넌트 마운트 시에만 실행


    return (
        <Layout>
        <Grid container spacing={2} style={{ maxWidth: '1300px', margin: '0 auto', padding: '10px', backgroundColor: "#ffffff" }}>
                {stockInfo && (
                    <>
                        <Grid item xs={12} style={{padding:0}} >
                            <Card raised elevation = {0} sx={{ mb: 4 }} style={{marginBottom:10}}>
                                <CardContent>
                                    <Typography variant="h6" component="h3" gutterBottom>
                                        {stockInfo.company_name} ({stockInfo.ticker})
                                    </Typography>
                                    <Box display="flex" justifyContent="flex-start" alignItems="center" gap={2}>
                                    <Typography variant="h5" component="h2" style={stockPrice ? change_rateStyle(stockPrice.change_rate) : {}} gutterBottom>
                                    {stockPrice ? stockPrice.close.toLocaleString() : '로딩 중'}원
                                    </Typography>
                                    <Typography variant="h5" component="h2" style={stockPrice ? change_rateStyle(stockPrice.change_rate) : {}} gutterBottom>
                                    {stockPrice && stockPrice.change_rate > 0 ? `(+${stockPrice.change_rate}%)` : `(${stockPrice.change_rate}%)`}
                                    </Typography>

                                    
                                    </Box>
                                    <Typography color="textSecondary" gutterBottom>
                                        시장: {stockInfo.market} | 섹터: {stockInfo.sector}
                                    </Typography>
                                    <Typography variant="body2" component="p">
                                        {stockInfo.company_description}
                                    </Typography>
                                </CardContent>
                            </Card>
                            <div className="DividingLine_line__gjUrd"></div>

                            <Paper elevation={0}  sx={{ p: 2 }}  style={{marginBottom:10}}>
                                <Box display="flex" flexWrap="wrap" justifyContent="space-around">
                                    {Object.entries({
                                        "시가 총액": `${stockInfo.market_cap.toLocaleString()}원`,
                                        "PER": stockInfo.per,
                                        "EPS": stockInfo.eps,
                                        "PBR": stockInfo.pbr,
                                        "BPS": stockInfo.bps,
                                        "배당금": `${stockInfo.divided}원`,
                                        "배당률": `${stockInfo.divided_rate}%`
                                    }).map(([key, value], index) => (
                                        <Box key={index} minWidth={100} textAlign="center">
                                            <Typography variant="subtitle2" borderBottom={ '1px solid #eee'} gutterBottom>
                                                {key}
                                            </Typography>
                                            <Typography variant="body2" color="textSecondary">
                                                {value}
                                            </Typography>
                                        </Box>
                                    ))}
                                </Box>
                            </Paper>
                            <div className="DividingLine_line__gjUrd"></div>
                            <h2> 주가(일봉)</h2>
                            <div ref={chartContainerRef} style={{ padding:"10px 0",margin: '0 auto', height: '400px' }} />
                            <div className="DividingLine_line__gjUrd"></div>

                            <h2> 날짜별 언급 추이</h2>
                            <div ref={chartContainerRef2} style={{ width: '100%', height: '300px' }} />
                        </Grid>

                        <div className="DividingLine_line__gjUrd"></div>
                        <Grid item xs={12} md={4} style={{paddingLeft:0}}>
                        <h2 style={{marginTop:0}}>관련 정치인 언급 순위</h2>
                        <FormControl fullWidth>
                            <InputLabel id="period-select-label">Period</InputLabel>
                            <Select
                            labelId="period-select-label"
                            id="period-select"
                            value={period5}
                            label="Period"
                            onChange={handlePeriodChange5}
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
                                <TableCell>Politician</TableCell>
                                <TableCell align="right">Count</TableCell>
                                <TableCell align="right">Period</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody  style={{minHeight:'585px'}}>
                                {data5.map((row) => (
                                <TableRow key={row.ranking}>
                                    <TableCell  component="th" scope="row">{row.ranking}</TableCell>
                                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("politician",row.name)}>{row.name}</TableCell>
                                    <TableCell align="right">{row.cnt}</TableCell>
                                    <TableCell align="right">{row.period}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                            </Table>
                        </TableContainer>
                        </Grid>


                        <div className="DividingLine_line__gjUrd"></div>
                        <Grid item xs={12} md={4} style={{paddingLeft:'10px'}}>
                        <h2 style={{marginTop:0}}>관련 테마 언급 순위</h2>
                        <FormControl fullWidth>
                            <InputLabel id="period-select-label">Period</InputLabel>
                            <Select
                            labelId="period-select-label"
                            id="period-select"
                            value={period6}
                            label="Period"
                            onChange={handlePeriodChange6}
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
                                <TableCell className="overtext" >thema</TableCell>
                                <TableCell align="right">Count</TableCell>
                                <TableCell align="right">Period</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody style={{minHeight:'585px'}}>
                                {data6.map((row) => (
                                <TableRow key={row.ranking}>
                                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                                    <TableCell style={{ cursor: 'pointer',fontWeight:"bold" }} onClick={() => handleNameClick("thema",row.name)}>{row.name}</TableCell>
                                    <TableCell align="right">{row.cnt}</TableCell>
                                    <TableCell align="right">{row.period}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                            </Table>
                        </TableContainer>
                        </Grid>

                        <div className="DividingLine_line__gjUrd"></div>
                        <Grid item xs={12} md={4} style={{paddingLeft:'10px'}}>
                        <h2 style={{marginTop:0}}>관련 업종 언급 순위</h2>
                        <FormControl fullWidth>
                            <InputLabel id="period-select-label">Period</InputLabel>
                            <Select
                            labelId="period-select-label"
                            id="period-select"
                            value={period7}
                            label="Period"
                            onChange={handlePeriodChange7}
                            >
                            <MenuItem value={1}>1</MenuItem>
                            <MenuItem value={7}>7</MenuItem>
                            <MenuItem value={30}>30</MenuItem>
                            <MenuItem value={60}>60</MenuItem>
                            <MenuItem value={180}>180</MenuItem>
                            <MenuItem value={365}>365</MenuItem>
                            </Select>
                        </FormControl>
                        <TableContainer component={Paper} className="childGrid">
                            <Table aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                <TableCell>Ranking</TableCell>
                                <TableCell>Sector</TableCell>
                                <TableCell align="right">Count</TableCell>
                                <TableCell align="right">Period</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody style={{minHeight:'585px'}}>
                                {data7.map((row) => (
                                <TableRow key={row.ranking}>
                                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("sector",row.name)}>{row.name}</TableCell>
                                    <TableCell align="right">{row.cnt}</TableCell>
                                    <TableCell align="right">{row.period}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                            </Table>
                        </TableContainer>
                        </Grid>


                    </>
                )}
            </Grid>


        </Layout>
    );
}

export default StockPage;