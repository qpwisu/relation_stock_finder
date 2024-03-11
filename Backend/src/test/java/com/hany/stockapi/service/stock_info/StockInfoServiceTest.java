package com.hany.stockapi.service.stock_info;

import com.hany.stockapi.dto.StockInfoDTO;
import com.hany.stockapi.mapper.ApiMapper;
import com.hany.stockapi.service.StockInfoService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class StockInfoServiceTest {

    @Mock
    private ApiMapper apiMapper;

    @InjectMocks
    private StockInfoService stockInfoService;

    @Test
    void getStockInfoByTicker() {
        // 준비
        String testTicker = "005490";
        StockInfoDTO expectedStockInfo = StockInfoDTO.builder()
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

        // Mockito를 사용해 ApiMapper의 동작을 모의합니다.
        when(apiMapper.findByTicker(testTicker)).thenReturn(expectedStockInfo);

        // 실행
        StockInfoDTO actualStockInfo = stockInfoService.getStockInfoByTicker(testTicker);

        // 검증
        assertNotNull(actualStockInfo, "StockInfoDTO는 null이 아니어야 합니다.");
        assertEquals(testTicker, actualStockInfo.getTicker(), "티커 값이 일치해야 합니다.");

        // Mockito가 예상대로 동작했는지 확인합니다.
        verify(apiMapper).findByTicker(testTicker);
    }
}
