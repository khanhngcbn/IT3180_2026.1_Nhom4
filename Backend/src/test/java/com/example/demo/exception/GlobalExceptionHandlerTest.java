package com.example.demo.exception;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import jakarta.validation.ConstraintViolationException;
import java.util.Collections;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;

class GlobalExceptionHandlerTest {

    private GlobalExceptionHandler handler;

    @BeforeEach
    void setUp() {
        handler = new GlobalExceptionHandler();
    }

    @Test
    void handleAccessDenied_returns403() {
        ResponseEntity<String> response = handler.handleAccessDenied(new AccessDeniedException("denied"));

        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());
        assertTrue(response.getBody().contains("không có quyền"));
    }

    @Test
    void handleUnreadable_returns400WithMessage() {
        ResponseEntity<Map<String, String>> response =
                handler.handleUnreadable(new HttpMessageNotReadableException("bad json", null, null));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertTrue(response.getBody().containsKey("message"));
    }

    @Test
    void handleConstraintViolation_returns400() {
        ResponseEntity<String> response = handler.handleConstraintViolation(
                new ConstraintViolationException("Invalid input", Collections.emptySet()));

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Invalid input", response.getBody());
    }

    @Test
    void handleAuthenticationException_returns401() {
        ResponseEntity<String> response =
                handler.handleAuthenticationException(new BadCredentialsException("Bad credentials"));

        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
        assertTrue(response.getBody().contains("Bad credentials"));
    }

    @Test
    void handleRuntimeException_returns500() {
        ResponseEntity<String> response = handler.handleRuntimeException(new RuntimeException("boom"));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertTrue(response.getBody().contains("boom"));
    }
}
