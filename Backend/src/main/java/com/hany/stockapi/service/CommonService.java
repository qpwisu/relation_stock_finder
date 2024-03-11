package com.hany.stockapi.service;

import com.hany.stockapi.mapper.ApiMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CommonService {
    private final ApiMapper apiMapper;

    @Autowired
    public CommonService(ApiMapper apiMapper) {
        this.apiMapper = apiMapper;
    }


    public List<String> getPolitician(String query){
        return apiMapper.findPolitician(query);
    }
    public List<String> getStock(String query){
        return apiMapper.findStock(query);
    }
    public List<String> getSector(String query){
        return apiMapper.findSector(query);
    }
    public List<String> getThema(String query){
        return apiMapper.findThema(query);
    }

}
