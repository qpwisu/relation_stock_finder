package com.hany.stockapi.dto;
import lombok.Builder;
import lombok.Data;

import java.sql.Date;

@Data
@Builder
public class StockPriceDTO {
    private Date date;
    private String ticker;
    private Float open;
    private Float high;
    private Float low;
    private Float close;
    private Float volume;
    private Float changeRate;
}

