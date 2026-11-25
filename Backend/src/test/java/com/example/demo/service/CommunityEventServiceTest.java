package com.example.demo.service;

import com.example.demo.service.CommunityEventService.CommunityEvent;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CommunityEventServiceTest {

    private final CommunityEventService service = new CommunityEventService();

    @Test
    void returnsOnlyEventsFromTodayOnwardInOrder() {
        LocalDate today = LocalDate.of(2026, 11, 26);

        List<CommunityEvent> events = service.upcoming(today, 5);

        assertEquals(5, events.size());
        for (int i = 0; i < events.size(); i++) {
            assertFalse(events.get(i).date().isBefore(today));
            if (i > 0) {
                assertFalse(events.get(i).date().isBefore(events.get(i - 1).date()));
            }
        }
        // 28/11/2026 là thứ bảy cuối tháng, 30/11/2026 là ngày làm việc cuối tháng
        assertEquals(LocalDate.of(2026, 11, 28), events.get(0).date());
        assertEquals("Ngày hội văn hóa", events.get(0).title());
        assertEquals(LocalDate.of(2026, 11, 30), events.get(1).date());
        assertEquals("Họp ban quản trị", events.get(1).title());
        // tiếp theo là sự kiện của tháng 12: chủ nhật đầu tiên 06/12/2026
        assertEquals(LocalDate.of(2026, 12, 6), events.get(2).date());
        assertEquals("Họp cư dân định kỳ", events.get(2).title());
    }

    @Test
    void decemberBoardMeetingReviewsTheYearlyBudget() {
        List<CommunityEvent> events = service.upcoming(LocalDate.of(2026, 12, 30), 1);

        assertEquals(LocalDate.of(2026, 12, 31), events.get(0).date());
        assertTrue(events.get(0).description().contains("năm 2026"));
    }

    @Test
    void limitIsClamped() {
        LocalDate today = LocalDate.of(2026, 1, 1);
        assertEquals(1, service.upcoming(today, 0).size());
        assertEquals(CommunityEventService.MAX_LIMIT, service.upcoming(today, 1000).size());
    }
}
