package com.hany.stockapi.dto;

import lombok.Builder;
import lombok.Data;

import java.sql.Date;

@Data
@Builder
public class BlogDTO {
    private String title;
    private String header;
    private String href;
    private Date date;
}
