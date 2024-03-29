package com.hany.stockapi.mapper;

import com.hany.stockapi.dto.*;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface ApiMapper {

    String findTickerBycompany_name(String company_name);
    List<StockPriceDTO> findPeriodPriceByTicker(String ticker);
    List<AggregateDTO> findAggregateCategory(String company_name,String category, Integer period);
    List<AggregateDTO> findAggregateStock(String name,String category, Integer period);

    List<DateAggregateDTO> findDateAggregateCategory(String name,String category);

    StockNowPriceDTO findPriceBycompany_name(String company_name);

    StockInfoDTO findStockBycompany_name(String company_name);
    List<CategoryTotalDTO> selectCategoryTotal(Integer period,String category);
    List<CategoryRelationStockTotalDTO> selectCategoryRelationStockTotal(Integer period,String category);
    List<StockNowPriceDTO> selectStockNowPriceDTO();

    List<BlogDTO> findBlogPolitician(String name,Integer offset);
    List<BlogDTO> findBlogThema(String name,Integer offset);
    List<BlogDTO> findBlogSector(String name,Integer offset);


    List<String> findStock(String query);
    List<String> findPolitician(String query);
    List<String> findThema(String query);
    List<String> findSector(String query);


}
