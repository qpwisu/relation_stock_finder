package com.hany.stockapi.controller;

import com.hany.stockapi.dto.*;
import com.hany.stockapi.service.StockInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
@RestController
@RequestMapping("/api/stock")
public class StockInfoController {
    private final StockInfoService stockInfoService;

    @Autowired
    public StockInfoController(StockInfoService stockInfoService) {
        this.stockInfoService = stockInfoService;
    }

    // 주식 정보 검색
    @GetMapping("/info")
    public ResponseEntity<ApiResponseDTO<StockInfoDTO>> getStockInfo(@RequestParam String company_name) {
        StockInfoDTO stockInfo = stockInfoService.getStockInfoBycompany_name(company_name);
        if (stockInfo == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(stockInfo));
    }
    @GetMapping("/price")
    public ResponseEntity<ApiResponseDTO<StockNowPriceDTO>> getStockPrice(@RequestParam String company_name) {
        StockNowPriceDTO stockPrice = stockInfoService.getPriceInfoBycompany_name(company_name);
        if (stockPrice == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(stockPrice));
    }

    @GetMapping("/price/period")
    public ResponseEntity<ApiResponseDTO<List<StockPriceDTO> >> getPeriodStockPrice(@RequestParam String company_name) {
        String ticker = stockInfoService.getTickerBycompany_name(company_name);
        List<StockPriceDTO>  stockPrice = stockInfoService.getPeriodPriceByTicker(ticker);
        if (stockPrice == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(stockPrice));
    }

    @GetMapping("/aggregate/category")
    public ResponseEntity<ApiResponseDTO<List<AggregateDTO> >> getAggregateCategory(@RequestParam String company_name,@RequestParam String category,@RequestParam Integer period) {
        List<AggregateDTO> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화
        ArrayList<Integer> allowedPeriods = new ArrayList<>(Arrays.asList(1,7,30,90,180));

        if (category.equals("politician") || category.equals("thema") || category.equals("sector")) {
            info = stockInfoService.getAggregateCategory(company_name,category,period);
        }
        else{
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("잘못된 경로입니다"));
        }

        if (!allowedPeriods.contains(period)) {
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("period는 1,7,30,60,180,365만 가능합니다."));
        }

        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }

    @GetMapping("/blog")
    public ResponseEntity<ApiResponseDTO<List<BlogDTO> >> getBlog(@RequestParam String name,@RequestParam String category,@RequestParam Integer page) {
        List<BlogDTO> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화

        Integer offset = (page-1) * 10;

        if (category.equals("politician")){
            info = stockInfoService.getBlogPolitician(name,offset);
        }
        else if (category.equals("thema")) {
            info = stockInfoService.getBlogThema(name,offset);
        }
        else if (category.equals("sector")) {
            info = stockInfoService.getBlogSector(name,offset);
        }
        else{
            return ResponseEntity.ok(ApiResponseDTO.ok(info));
        }

        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }


    @GetMapping("/aggregate/stock")
    public ResponseEntity<ApiResponseDTO<List<AggregateDTO> >> getAggregateStock(@RequestParam String name,@RequestParam String category,@RequestParam Integer period) {
        List<AggregateDTO> info = stockInfoService.getAggregateStock(name,category,period);
        ArrayList<Integer> allowedPeriods = new ArrayList<>(Arrays.asList(1,7,30,90,180));
        if (!allowedPeriods.contains(period)) {
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("period는 1,7,30,60,180,365만 가능합니다."));
        }
        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();

        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }

    @GetMapping("/aggregate/date/category")
    public ResponseEntity<ApiResponseDTO<List<DateAggregateDTO> >> getDateAggregateCategory(@RequestParam String name,@RequestParam String category) {
        List<DateAggregateDTO> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화

        if (category.equals("stock") || category.equals("politician") || category.equals("thema") || category.equals("sector")) {
            info = stockInfoService.getDateAggregateCategory(name,category);
        }
        else{
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("잘못된 경로입니다"));
        }

        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();

        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }


    @GetMapping("/total/category")
    public ResponseEntity<ApiResponseDTO<List<CategoryTotalDTO>>>  getCategoryTotal(@RequestParam String category,@RequestParam Integer period) {
        ArrayList<Integer> allowedPeriods = new ArrayList<>(Arrays.asList(1,7,30,90,180));
        List<CategoryTotalDTO> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화

        if (category.equals("politician") || category.equals("thema") || category.equals("sector")) {
            info = stockInfoService.getCategoryTotal(period, category);
        }
        else{
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("잘못된 경로입니다"));
        }

        if (!allowedPeriods.contains(period)) {
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("period는 1,7,30,60,180,365만 가능합니다."));
        }

        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();

        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }

    @GetMapping("/total/stock")
    public ResponseEntity<ApiResponseDTO<List<CategoryRelationStockTotalDTO>>> getCategoryStockTotal(@RequestParam String category,@RequestParam Integer period) {
        ArrayList<Integer> allowedPeriods = new ArrayList<>(Arrays.asList(1,7,30,90,180));
        List<CategoryRelationStockTotalDTO> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화

        if (category.equals("politician") || category.equals("thema") || category.equals("sector")) {
            info = stockInfoService.getCategoryRelationStockTotal(period,category);
        }
        else{
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("잘못된 경로입니다"));
        }

        if (!allowedPeriods.contains(period)) {
            return ResponseEntity.badRequest().body(ApiResponseDTO.error("period는 1,7,30,60,180,365만 가능합니다."));
        }

        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }

    @GetMapping("/total/price")
    public ResponseEntity<ApiResponseDTO<List<StockNowPriceDTO>>> getStockTotal() {
        ArrayList<Integer> allowedPeriods = new ArrayList<>(Arrays.asList(1,7,30,90,180));

        List<StockNowPriceDTO> info = stockInfoService.getStockNowPriceDTO();
        if (info == null || info.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(ApiResponseDTO.ok(info));
    }
}
