package com.example.demo.validation;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import jakarta.validation.ConstraintValidatorContext;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ValidPasswordValidatorTest {

    private ValidPasswordValidator validator;
    private ConstraintValidatorContext context;
    private ConstraintValidatorContext.ConstraintViolationBuilder builder;

    @BeforeEach
    void setUp() {
        validator = new ValidPasswordValidator();
        context = mock(ConstraintValidatorContext.class);
        builder = mock(ConstraintValidatorContext.ConstraintViolationBuilder.class);
        when(context.buildConstraintViolationWithTemplate(anyString())).thenReturn(builder);
        when(builder.addConstraintViolation()).thenReturn(context);
    }

    @Test
    void isValid_acceptsStrongPassword() {
        assertTrue(validator.isValid("Str0ng!Pass", context));
    }

    @Test
    void isValid_rejectsShortPassword() {
        assertFalse(validator.isValid("Ab1!", context));
        verify(context).disableDefaultConstraintViolation();
    }

    @Test
    void isValid_rejectsMissingSpecialCharacter() {
        assertFalse(validator.isValid("StrongPass1", context));
    }

    @Test
    void isValid_rejectsWhitespace() {
        assertFalse(validator.isValid("Str0ng !Pass", context));
    }

    @Test
    void isValid_rejectsSequentialNumbers() {
        assertFalse(validator.isValid("Aa!12345x", context));
    }
}
