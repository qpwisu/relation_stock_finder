package com.hany.stockapi.service;

import com.hany.stockapi.dto.*;
import com.hany.stockapi.mapper.ApiMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockInfoService {
    private final ApiMapper apiMapper;

    @Autowired
    public StockInfoService(ApiMapper apiMapper) {
        this.apiMapper = apiMapper;
    }

    public String getTickerByCompanyName(String companyName){
        return apiMapper.findTickerByCompanyName(companyName);
    }
    public List<StockPriceDTO>  getPeriodPriceByTicker(String ticker) {
        return apiMapper.findPeriodPriceByTicker(ticker);
    }
    public List<AggregateDTO>  getAggregateCategory(String companyName, String category, Integer period) {
        return apiMapper.findAggregateCategory(companyName,category,period);
    }


    public List<AggregateDTO>  getAggregateStock(String name, String category, Integer period) {
        return apiMapper.findAggregateStock(name,category,period);
    }

    public List<DateAggregateDTO>  getDateAggregateCategory(String name, String category) {
        return apiMapper.findDateAggregateCategory(name,category);
    }
    public StockNowPriceDTO getPriceInfoByCompanyName(String companyName) {
        return apiMapper.findPriceByCompanyName(companyName);
    }
    public StockInfoDTO getStockInfoByCompanyName(String companyName) {
        return apiMapper.findStockByCompanyName(companyName);
    }



    public List<CategoryTotalDTO> getCategoryTotal(Integer period, String category) {
        return apiMapper.selectCategoryTotal(period, category);
    }
    public List<CategoryRelationStockTotalDTO> getCategoryRelationStockTotal(Integer period, String category) {
        return apiMapper.selectCategoryRelationStockTotal(period, category);
    }

    public List<StockNowPriceDTO> getStockNowPriceDTO(){
        return apiMapper.selectStockNowPriceDTO();
    }

    public List<BlogDTO> getBlogPolitician(String name,Integer offset){
        return apiMapper.findBlogPolitician(name,offset);
    }
    public List<BlogDTO> getBlogSector(String name,Integer offset){
        return apiMapper.findBlogSector(name,offset);
    }
    public List<BlogDTO> getBlogThema(String name,Integer offset){
        return apiMapper.findBlogThema(name,offset);
    }
}