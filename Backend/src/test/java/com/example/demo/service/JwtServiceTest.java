package com.example.demo.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.jsonwebtoken.JwtException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

class JwtServiceTest {

    private static final String TEST_SECRET = "dGVzdC1zZWNyZXQtdGVzdC1zZWNyZXQtdGVzdC1zZWNyZXQtMTIzNDU2";

    private JwtService jwtService;

    @BeforeEach
    void setUp() {
        jwtService = new JwtService();
        ReflectionTestUtils.setField(jwtService, "secretKey", TEST_SECRET);
        ReflectionTestUtils.setField(jwtService, "jwtExpiration", 3600000L);
        jwtService.initKey();
    }

    @Test
    void generateToken_embedsUsernameAndRole() {
        String token = jwtService.generateToken("admin@example.com", "ADMIN");

        assertNotNull(token);
        assertEquals("admin@example.com", jwtService.extractUsername(token));
        assertEquals("ADMIN", jwtService.extractRole(token));
    }

    @Test
    void extractUsername_throwsOnTamperedToken() {
        String token = jwtService.generateToken("user@example.com", "USER");
        String tampered = token + "corrupted";

        assertThrows(JwtException.class, () -> jwtService.extractUsername(tampered));
    }

    @Test
    void extractUsername_throwsOnMalformedToken() {
        assertThrows(JwtException.class, () -> jwtService.extractUsername("not-a-valid-jwt"));
    }
}
