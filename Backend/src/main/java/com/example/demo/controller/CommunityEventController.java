package com.example.demo.controller;

import com.example.demo.service.CommunityEventService;
import com.example.demo.service.CommunityEventService.CommunityEvent;
import com.example.demo.util.AppClock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/** Sự kiện cộng đồng sắp tới, hiển thị ở trang chủ của Ban quản lý và cư dân. */
@RestController
@RequestMapping("/api/events")
public class CommunityEventController {

    @Autowired
    private CommunityEventService eventService;

    @GetMapping("/upcoming")
    public List<CommunityEvent> upcoming(@RequestParam(defaultValue = "5") int limit) {
        return eventService.upcoming(AppClock.today(), limit);
    }
}
