package com.hany.stockapi.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AggregateDTO {
    private String company_name;
    private String name;
    private int cnt; // 언급된 횟수를 나타냅니다. 이는 특정 기간 동안 정치인이 언급된 총 횟수를 의미합니다.
    private int ranking;
    private int period; // 기간을 나타냅니다. 7,30,60,180,365 기간이 있습니다.
    private String category;
}
