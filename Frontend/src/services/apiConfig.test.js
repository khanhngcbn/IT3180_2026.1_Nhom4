import api from "./apiConfig";

describe("apiConfig", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("configures default baseURL and JSON content-type header", () => {
    expect(api.defaults.baseURL).toBe("http://localhost:9090/api");
    expect(api.defaults.headers["Content-Type"]).toBe("application/json");
  });

  test("request interceptor attaches Bearer token when present in localStorage", () => {
    localStorage.setItem("token", "sample-jwt-token");
    const requestInterceptor = api.interceptors.request.handlers[0].fulfilled;

    const config = requestInterceptor({ headers: {} });

    expect(config.headers.Authorization).toBe("Bearer sample-jwt-token");
  });

  test("request interceptor leaves Authorization unset when no token exists", () => {
    const requestInterceptor = api.interceptors.request.handlers[0].fulfilled;

    const config = requestInterceptor({ headers: {} });

    expect(config.headers.Authorization).toBeUndefined();
  });
});
