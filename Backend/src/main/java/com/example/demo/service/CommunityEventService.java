package com.example.demo.service;

import org.springframework.stereotype.Service;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.YearMonth;
import java.time.temporal.TemporalAdjusters;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Lịch sự kiện cộng đồng của chung cư. Các sự kiện lặp lại hằng tháng theo quy tắc cố định,
 * nên ngày luôn được tính từ ngày hiện tại thay vì ghi cứng.
 */
@Service
public class CommunityEventService {

    public static final int MAX_LIMIT = 20;

    public record CommunityEvent(LocalDate date, LocalTime time, String title, String description) {
    }

    /** Các sự kiện từ hôm nay trở đi (tính cả hôm nay), sắp theo thời gian. */
    public List<CommunityEvent> upcoming(LocalDate today, int limit) {
        int size = Math.max(1, Math.min(limit, MAX_LIMIT));
        List<CommunityEvent> result = new ArrayList<>();
        YearMonth month = YearMonth.from(today);
        while (result.size() < size) {
            eventsOf(month).stream()
                    .filter(e -> !e.date().isBefore(today))
                    .forEach(result::add);
            month = month.plusMonths(1);
        }
        result.sort(Comparator.comparing(CommunityEvent::date).thenComparing(CommunityEvent::time));
        return result.subList(0, size);
    }

    List<CommunityEvent> eventsOf(YearMonth month) {
        LocalDate first = month.atDay(1);
        String monthText = String.format("%02d/%d", month.getMonthValue(), month.getYear());
        boolean december = month.getMonthValue() == 12;

        return List.of(
                new CommunityEvent(nthDayOfWeek(first, 1, DayOfWeek.SUNDAY), LocalTime.of(9, 0),
                        "Họp cư dân định kỳ",
                        "Thảo luận về quy định chung và kế hoạch bảo trì tháng " + monthText + "."),
                new CommunityEvent(nthDayOfWeek(first, 2, DayOfWeek.SATURDAY), LocalTime.of(7, 30),
                        "Dọn dẹp cộng đồng",
                        "Hoạt động làm sạch khu vực chung cư."),
                new CommunityEvent(nthDayOfWeek(first, 3, DayOfWeek.SUNDAY), LocalTime.of(16, 0),
                        "Ngày hội gia đình",
                        "Sự kiện ngoài trời với trò chơi và tiệc BBQ."),
                new CommunityEvent(first.with(TemporalAdjusters.lastInMonth(DayOfWeek.SATURDAY)), LocalTime.of(18, 0),
                        "Ngày hội văn hóa",
                        "Trình diễn nghệ thuật và ẩm thực địa phương."),
                new CommunityEvent(lastWorkingDay(month), LocalTime.of(14, 0),
                        "Họp ban quản trị",
                        december
                                ? "Xem xét ngân sách năm " + month.getYear() + " và kế hoạch năm mới."
                                : "Xem xét thu chi tháng " + monthText + " và kế hoạch tháng tới.")
        );
    }

    private static LocalDate nthDayOfWeek(LocalDate firstOfMonth, int n, DayOfWeek day) {
        return firstOfMonth.with(TemporalAdjusters.dayOfWeekInMonth(n, day));
    }

    private static LocalDate lastWorkingDay(YearMonth month) {
        LocalDate date = month.atEndOfMonth();
        while (date.getDayOfWeek() == DayOfWeek.SATURDAY || date.getDayOfWeek() == DayOfWeek.SUNDAY) {
            date = date.minusDays(1);
        }
        return date;
    }
}
