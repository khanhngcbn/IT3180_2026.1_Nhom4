import api from "services/apiConfig";
import {
  EVENT_PAGE_SIZE,
  fetchUpcomingEvents,
  formatEventDate,
  formatEventTime,
} from "./eventService";

jest.mock("services/apiConfig", () => ({
  get: jest.fn(),
}));

describe("eventService", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("formatEventDate converts ISO date to dd/MM/yyyy", () => {
    expect(formatEventDate("2026-11-28")).toBe("28/11/2026");
    expect(formatEventDate("")).toBe("");
    expect(formatEventDate(null)).toBe("");
  });

  test("formatEventTime slices HH:mm:ss to HH:mm", () => {
    expect(formatEventTime("18:30:00")).toBe("18:30");
    expect(formatEventTime("")).toBe("");
    expect(formatEventTime(undefined)).toBe("");
  });

  test("fetchUpcomingEvents calls /events/upcoming with limit and returns array", async () => {
    const events = [{ id: 1, title: "Community Meeting" }];
    api.get.mockResolvedValueOnce({ data: events });

    const result = await fetchUpcomingEvents(10);

    expect(api.get).toHaveBeenCalledWith("/events/upcoming", { params: { limit: 10 } });
    expect(result).toEqual(events);
  });

  test("fetchUpcomingEvents uses default page size and returns empty array on non-array payload", async () => {
    api.get.mockResolvedValueOnce({ data: null });

    const result = await fetchUpcomingEvents();

    expect(api.get).toHaveBeenCalledWith("/events/upcoming", {
      params: { limit: EVENT_PAGE_SIZE },
    });
    expect(result).toEqual([]);
  });
});
