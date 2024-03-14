import '../App.css';
import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Select, MenuItem, FormControl, InputLabel,Grid } from '@mui/material';
import Layout from '../Layout';
import '../myCss.css';
import { useNavigate } from 'react-router-dom';

import {useFetchPoliticianTotalData, useFetchStockTotalData,useFetchStockPriceData} from '../useFetchData.js'; // 커스텀 훅 임포트
function FirstPage() {
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


  const [period, setPeriod] = useState(7);
  const [period2, setPeriod2] = useState(7);
  const [period4, setPeriod4] = useState(7);
  const [period5, setPeriod5] = useState(7);
  const [period6, setPeriod6] = useState(7);
  const [period7, setPeriod7] = useState(7);


  // 커스텀 훅 사용
  const data3 = useFetchStockPriceData(); 

  const data= useFetchPoliticianTotalData("politician",period); 
  const data2 = useFetchStockTotalData("politician",period2); 

  const data4= useFetchPoliticianTotalData("thema",period4); 
  const data5 = useFetchStockTotalData("thema",period5); 
  const data6= useFetchPoliticianTotalData("sector",period6); 

  const data7 = useFetchStockTotalData("sector",period7); 

  // Period 변경을 핸들링하는 함수
  const handlePeriodChange = (event) => {
    setPeriod(event.target.value);
  };

  // Period 변경을 핸들링하는 함수
  const handlePeriodChange2 = (event) => {
    setPeriod2(event.target.value);
  };

  const handlePeriodChange4 = (event) => {
    setPeriod4(event.target.value);
  };

  // Period 변경을 핸들링하는 함수
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

  return (
    <Layout>

        <Grid container spacing={2} style={{ maxWidth: '1300px', margin: '0 auto', padding: '18px 20px 13px', backgroundColor: "#ffffff" }}>

        <Grid item xs={12} md={12} style={{paddingLeft:0}}>
          <h2 style={{marginTop:0}}>실시간 급상승 종목</h2>
          <TableContainer component={Paper} className="childGrid">
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Ticker</TableCell>
                  <TableCell>company_name</TableCell>
                  <TableCell align="right">Close</TableCell>
                  <TableCell align="right">ChangeRate</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data3.map((row) => (
                  <TableRow key={row.ticker}>
                    <TableCell component="th" scope="row">{row.ticker}</TableCell>
                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("stock",row.company_name)}>{row.company_name}</TableCell>
                    <TableCell align="right">{row.close}</TableCell>
                    <TableCell align="right" style={{color:"red",fontWeight:"bold"}}>{row.changeRate}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        <div className="DividingLine_line__gjUrd"></div>
        <Grid item xs={12} md={4} style={{paddingLeft:0}}>
          <h2 style={{marginTop:0}}>주식 관련 정치인 언급 순위</h2>
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
          <TableContainer component={Paper} className="childGrid" >
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Ranking</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody >
                {data.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer',fontWeight:"bold" }} onClick={() => handleNameClick("politician",row.name)}>{row.name}</TableCell>
                    <TableCell align="right">{row.cnt}</TableCell>
                    <TableCell align="right">{row.period}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

       


        <div className="DividingLine_line__gjUrd"></div>
        <Grid item xs={12} md={4} style={{paddingLeft:10}}>
          <h2 style={{marginTop:0}}>주식 테마 언급 순위</h2>
          <FormControl fullWidth>
            <InputLabel id="period-select-label">Period</InputLabel>
            <Select
              labelId="period-select-label"
              id="period-select"
              value={period4}
              label="Period"
              onChange={handlePeriodChange4}
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
                  <TableCell>Name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data4.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("thema",row.name)}>{row.name}</TableCell>
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
          <h2 style={{marginTop:0}}>주식 업종 언급 순위</h2>
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
                  <TableCell>Name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data6.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer',fontWeight:"bold" }} onClick={() => handleNameClick("sector",row.name)}>{row.name}</TableCell>
                    <TableCell align="right">{row.cnt}</TableCell>
                    <TableCell align="right">{row.period}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>



        <div className="DividingLine_line__gjUrd"></div>
        <Grid item xs={12} md={4} style={{paddingLeft:"0"}}>

          <h2 style={{marginTop:0}}>정치인 관련 주식 언급 순위</h2>
          <FormControl fullWidth>
            <InputLabel id="period-select-label">Period</InputLabel>
            <Select
              labelId="period-select-label"
              id="period-select"
              value={period2}
              label="Period"
              onChange={handlePeriodChange2}
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
                  <TableCell>company_name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data2.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer',fontWeight:"bold" }} onClick={() => handleNameClick("stock",row.company_name)}>{row.company_name}</TableCell>
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
          <h2 style={{marginTop:0}}>테마 관련 주식 언급 순위</h2>
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
                  <TableCell>company_name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data5.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer' ,fontWeight:"bold"}} onClick={() => handleNameClick("stock",row.company_name)}>{row.company_name}</TableCell>
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
          <h2 style={{marginTop:0}}>업종 관련 주식 언급 순위</h2>
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
              <MenuItem value={60}>90</MenuItem>
              <MenuItem value={180}>180</MenuItem>
            </Select>
          </FormControl>
          <TableContainer component={Paper} className="childGrid">
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Ranking</TableCell>
                  <TableCell>company_name</TableCell>
                  <TableCell align="right">Count</TableCell>
                  <TableCell align="right">Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data7.map((row) => (
                  <TableRow key={row.ranking}>
                    <TableCell component="th" scope="row">{row.ranking}</TableCell>
                    <TableCell style={{ cursor: 'pointer',fontWeight:"bold" }} onClick={() => handleNameClick("stock",row.company_name)}>{row.company_name}</TableCell>
                    <TableCell align="right">{row.cnt}</TableCell>
                    <TableCell align="right">{row.period}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        </Grid>

        
  </Layout>

  );
}

export default FirstPage;