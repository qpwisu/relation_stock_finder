package com.hany.stockapi.controller;

import com.hany.stockapi.dto.StockInfoDTO;
import com.hany.stockapi.service.StockInfoService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.math.BigDecimal;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class StockInfoControllerTest {

    @Mock
    private StockInfoService stockInfoService;

    @InjectMocks
    private StockInfoController stockInfoController;

    private MockMvc mockMvc;

    @BeforeEach //test 시작전 실행
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(stockInfoController).build();
    }

    @Test
    void getStockInfo_ReturnsStockInfo() throws Exception {
        // 준비
        String testTicker = "005490";
        StockInfoDTO mockStockInfo = StockInfoDTO.builder()
                .ticker("005490")
                .companyName("신성통상")
                .market("KOSPI")
                .companyDescription("동사는 1968년 설립된 이후 니트의류 수출기업으로서 주문자상표부착(OEM)방식의 수출을 영위, 현재 Target, WalMart 등 대형 Buyer 위주로 영업을 전개하고 있으며, 신규 Buyer 확보함.\n동사의 핵심 생산기지인 Nicaragua 중남미 현지법인과 더불어 Vietnam에 소재한 현지법인에 대규모 신·증설을 추진.\n신규 Buyer와의 Direct 영업을 통해 수익성을 개선함으로서 활발한 영업을 전개.")
                .sector("섬유,의류,신발,호화품")
                .marketCap(BigDecimal.valueOf(284300000000.00))
                .per(4.27F)
                .eps(463.0F)
                .pbr(0.69F)
                .bps(2879.0F)
                .divided(50.0F)
                .dividedRate(2.53F)
                .build();


        given(stockInfoService.getStockInfoByTicker(testTicker)).willReturn(mockStockInfo);

        // 실행 & 검증
        mockMvc.perform(get("/api/stocks/info")
                        .param("ticker", testTicker)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.ticker").value(testTicker));
    }

    @Test
    void getStockInfo_ReturnsNotFound() throws Exception {
        // 준비
        String testTicker = "invalidTicker";
        given(stockInfoService.getStockInfoByTicker(testTicker)).willReturn(null);

        // 실행 & 검증
        mockMvc.perform(get("/api/stocks/info")
                        .param("ticker", testTicker)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
    }
}
