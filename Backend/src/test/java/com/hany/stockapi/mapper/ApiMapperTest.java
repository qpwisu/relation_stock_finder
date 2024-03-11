package com.hany.stockapi.mapper;
import com.hany.stockapi.dto.StockInfoDTO;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.springframework.test.util.AssertionErrors.assertEquals;

@ExtendWith(SpringExtension.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@MybatisTest
public class ApiMapperTest {

    @Autowired
    private ApiMapper apiMapper;

    @Test
    public void findByTickerTest() {
        // 테스트 로직
        String testTicker = "005490";
        StockInfoDTO result = apiMapper.findByTicker(testTicker);
        assertNotNull(result, "StockInfoDTO는 null이 아니어야 합니다.");
        assertEquals("티커 값이 일치해야 합니다.","005490", result.getTicker());
    }
}
