package com.hany.stockapi.dto;

import lombok.Builder;
import lombok.Data;

import java.sql.Date;

@Data
@Builder
public class DateAggregateDTO {
    private String category;
    private String name;
    private Date date;
    private int cnt; // 언급된 횟수를 나타냅니다. 이는 특정 기간 동안 정치인이 언급된 총 횟수를 의미합니다.
}
