package com.hany.stockapi.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class StockNowPriceDTO {
    private String ticker;
    private String companyName;
    private Float close;
    private Float changeRate;
}
