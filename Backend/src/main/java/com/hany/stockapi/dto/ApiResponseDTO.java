package com.hany.stockapi.dto;
import lombok.Builder;
import lombok.Data;
@Data
@Builder
public class ApiResponseDTO<T> {
    private boolean success;
    private String message;
    private T data;

    public ApiResponseDTO(boolean success, String message, T data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }

    public static <T> ApiResponseDTO<T> ok(T data) {
        return new ApiResponseDTO<>(true, "Success", data);
    }

    public static <T> ApiResponseDTO<T> error(String message) {
        return new ApiResponseDTO<>(false, message, null);
    }

    // getters and setters
}