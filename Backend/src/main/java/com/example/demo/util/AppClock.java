package com.example.demo.util;

import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/** Ngày giờ theo múi giờ Việt Nam, dùng chung cho toàn hệ thống. */
public final class AppClock {

    public static final ZoneId ZONE = ZoneId.of("Asia/Ho_Chi_Minh");
    public static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("dd/MM/yyyy");

    private AppClock() {
    }

    public static LocalDate today() {
        return LocalDate.now(ZONE);
    }

    /** Ngày hôm nay dạng dd/MM/yyyy. */
    public static String todayText() {
        return today().format(DATE_FORMAT);
    }
}
