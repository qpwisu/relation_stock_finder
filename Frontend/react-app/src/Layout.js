// Layout.js
import React, { useState,useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from './logo.png'; // 로고 이미지 경로에 맞게 조정해주세요.
import { Box, FormControl, InputLabel, Select, MenuItem, Divider, TextField, Button } from '@mui/material';
import axios from 'axios';

const Layout = ({ children }) => {
    const navigate = useNavigate(); // useNavigate 훅을 사용
    // 이미지 클릭 핸들러
    const handleClick = () => {
        navigate('/'); // 루트 경로로 이동
    };

    const [searchType, setSearchType] = useState('stock');
    const [searchTerm, setSearchTerm] = useState('');
    const [suggestions, setSuggestions] = useState([]);


    const handleSearch = () => {
        // searchTerm이 suggestions 배열에 포함되어 있는지 확인
        const isTermInSuggestions = suggestions.includes(searchTerm);

        // searchTerm이 suggestions에 없으면 아무것도 하지 않고 반환
        if (!isTermInSuggestions) {
            alert("선택된 항목이 자동완성 목록에 없습니다.");
            return;
        }
        switch(searchType) {
            case 'thema':
                navigate('/thema', { state: { searchTerm: searchTerm } });
                break;
            case 'politician':
                navigate('/politician', { state: { searchTerm: searchTerm } });
                break;
            case 'stock':
                navigate('/stock', { state: { searchTerm: searchTerm } });
                break;
            case 'sector':
                navigate('/sector', { state: { searchTerm: searchTerm } });
                break;
            default:
                console.log('Unknown search type');
        }
    };

    useEffect(() => {
        if (searchTerm.length >= 1) { // 사용자가 2글자 이상 입력했을 때만 요청
            axios.get(`http://localhost:8081/api/common/autocomplete?query=${searchTerm}&category=${searchType}`)
                .then(response => {
                    setSuggestions(response.data);
                })
                .catch(error => {
                    console.error("There was an error!", error);
                });
        }
    }, [searchTerm,searchType]);


    return (
        <div className="FirstPage"  style={{backgroundColor:"#f3f5f7" }}>
            <div style={{
            backgroundColor: "#ffffff",
            display: "flex",
            alignItems: "center", // 세로 중앙 정렬
            cursor: "pointer",
            padding: "10px 20px"
            }} onClick={handleClick}>
            <img src={logo} alt="Logo" style={{ width: "150px", height: "30px" }} />
            <div style={{ fontWeight: "bold", marginLeft: "10px" }}>Beta</div> {/* 이미지 옆에 텍스트 추가 */}
            </div>

            <div>
                <Box position ="relative" sx={{ display: 'flex', alignItems: 'center', padding: '10px', borderRadius: '50px', backgroundColor: '#ffffff', maxWidth: '770px', margin: '20px auto', border: 1, borderColor: '#1976D2' }}>
                <FormControl sx={{ minWidth: 90, mr: 1 }}>
                    <InputLabel id="search-type-select-label" size="small">검색 유형</InputLabel>
                    <Select labelId="search-type-select-label" id="search-type-select" value={searchType} onChange={(e) => setSearchType(e.target.value)} size="small" sx={{ "& .MuiOutlinedInput-notchedOutline": { border: "none" } }}>
                        <MenuItem value="sector">섹터</MenuItem>
                        <MenuItem value="thema">테마</MenuItem>
                        <MenuItem value="politician">정치인</MenuItem>
                        <MenuItem value="stock">종목명</MenuItem>
                    </Select>
                </FormControl>
                <Divider orientation="vertical" flexItem sx={{ borderRightWidth: 2, borderColor: 'grey.500' }} />
                <TextField variant="outlined" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} sx={{ flexGrow: 1, mx: 1, "& .MuiOutlinedInput-notchedOutline": { border: "none" }}} size="small" placeholder='선택한 검색 유형을 검색' />
                <ul style={{
                    listStyleType: "none",
                    padding: 0,
                    margin: 0,
                    position: "absolute",
                    top: "100%", // 검색창 바로 아래에 위치하도록 조정
                    left: 0, // 왼쪽 정렬
                    backgroundColor: "#fff",
                    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
                    borderRadius: "4px",
                    width: "calc(100% - 2px)", // 경계선을 고려하여 너비 조정
                    zIndex: 1000,
                }}>
                    {suggestions.map((suggestion, index) => (
                        <li key={index} style={{
                            padding: "8px 16px",
                            cursor: "pointer",
                            borderBottom: "1px solid #ddd",
                            "&:last-child": {
                                borderBottom: "none",
                            },
                            "&:hover": {
                                backgroundColor: "#f5f5f5",
                            },
                        }} onClick={() => setSearchTerm(suggestion)}>
                            {suggestion}
                        </li>
                    ))}
                </ul>
                <Divider orientation="vertical" flexItem sx={{ borderRightWidth: 2, borderColor: 'grey.500' }} />
                <Button
                    variant="contained"
                    onClick={handleSearch}
                    disabled={!suggestions.includes(searchTerm)} // searchTerm이 suggestions 배열에 없으면 버튼 비활성화
                    sx={{ borderRadius: '50px', ml: 1 }}
                >
                    검색
                </Button>                
                </Box>
                <main>{children}</main>
            </div>


        </div>
    );
};

export default Layout;