package com.hany.stockapi.controller;

import com.hany.stockapi.service.CommonService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;


@RestController
@RequestMapping("/api/common")
public class CommonController {

    private final CommonService commonService;

    public CommonController(CommonService commonService) {
        this.commonService = commonService;
    }

    @GetMapping("/autocomplete")
    public ResponseEntity<List<String>> autoComplete(@RequestParam String query,@RequestParam String category) {
        // query에 기반하여 검색 제안을 찾는 로직 구현
        List<String> info = new ArrayList<>(); // `info`를 메소드의 시작 부분에서 선언 및 초기화
        if (category.equals("politician")){
            info = commonService.getPolitician(query);
        }
        else if (category.equals("stock")) {
            info = commonService.getStock(query);
        }
        else if (category.equals("thema")) {
            info = commonService.getThema(query);
        }
        else if (category.equals("sector")) {
            info = commonService.getSector(query);
        }
        else{
            return ResponseEntity.ok(info);
        }
        return ResponseEntity.ok(info);
    }
}
