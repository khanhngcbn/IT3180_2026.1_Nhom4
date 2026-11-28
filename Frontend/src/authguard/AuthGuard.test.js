import React from "react";
import { render, screen } from "@testing-library/react";
import AuthGuard from "./AuthGuard";

const mockNavigate = jest.fn();
const mockToast = jest.fn();

jest.mock("react-router-dom", () => ({
  useNavigate: () => mockNavigate,
}));

jest.mock("@chakra-ui/react", () => ({
  useToast: () => mockToast,
}));

const createJwt = (payload) => {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = btoa(JSON.stringify(payload));
  return `${header}.${body}.signature`;
};

describe("AuthGuard", () => {
  beforeEach(() => {
    localStorage.clear();
    mockNavigate.mockClear();
    mockToast.mockClear();
  });

  test("redirects to sign-in when no token is present", () => {
    render(
      <AuthGuard>
        <div>Protected Content</div>
      </AuthGuard>
    );

    expect(mockToast).toHaveBeenCalledTimes(1);
    expect(mockNavigate).toHaveBeenCalledWith("/auth/sign-in", { replace: true });
  });

  test("redirects to sign-in when token is expired", () => {
    const expiredToken = createJwt({ exp: Math.floor(Date.now() / 1000) - 60 });
    localStorage.setItem("token", expiredToken);

    render(
      <AuthGuard>
        <div>Protected Content</div>
      </AuthGuard>
    );

    expect(mockToast).toHaveBeenCalledTimes(1);
    expect(mockNavigate).toHaveBeenCalledWith("/auth/sign-in", { replace: true });
  });

  test("redirects to sign-in when token is malformed", () => {
    localStorage.setItem("token", "not-a-jwt");

    render(
      <AuthGuard>
        <div>Protected Content</div>
      </AuthGuard>
    );

    expect(mockNavigate).toHaveBeenCalledWith("/auth/sign-in", { replace: true });
  });

  test("renders children without redirecting when token is valid", () => {
    const validToken = createJwt({ exp: Math.floor(Date.now() / 1000) + 3600 });
    localStorage.setItem("token", validToken);

    render(
      <AuthGuard>
        <div>Protected Content</div>
      </AuthGuard>
    );

    expect(screen.getByText("Protected Content")).toBeInTheDocument();
    expect(mockNavigate).not.toHaveBeenCalled();
    expect(mockToast).not.toHaveBeenCalled();
  });
});
