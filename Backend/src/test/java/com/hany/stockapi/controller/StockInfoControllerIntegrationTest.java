package com.hany.stockapi.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.http.MediaType;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

@SpringBootTest
@AutoConfigureMockMvc
class StockInfoControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void getStockInfo_ReturnsStockInfo() throws Exception {
        String testTicker = "005490";
        mockMvc.perform(get("/api/stocks/info")
                        .param("ticker", testTicker)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$.ticker").value(testTicker));
    }

    @Test
    void getStockInfo_ReturnsNotFound() throws Exception {
        String testTicker = "invalidTicker";
        mockMvc.perform(get("/api/stocks/info")
                        .param("ticker", testTicker)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.status().isNotFound());
    }
}
