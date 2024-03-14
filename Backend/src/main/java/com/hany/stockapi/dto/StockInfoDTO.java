package com.hany.stockapi.dto;

import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
@Data
@Builder
public class StockInfoDTO {
    private String ticker;
    private String company_name;
    private String market;
    private String company_description;
    private String sector;
    private BigDecimal market_cap;
    private Float per;
    private Float eps;
    private Float pbr;
    private Float bps;
    private Float divided;
    private Float divided_rate;
    // 여기에 getter와 setter 메소드를 추가합니다.
}
