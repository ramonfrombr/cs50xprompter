"use client";
import { useContext, ReactNode, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { useRouter } from "next/navigation";

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { token } = useContext(AuthContext);
  const [isLoaded, setIsLoaded] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Wait for AuthContext to load token from localStorage
    setIsLoaded(true);
  }, []);

  useEffect(() => {
    if (isLoaded && !token) router.push("/auth/login");
  }, [isLoaded, token, router]);

  if (!isLoaded) return null;
  if (!token) return null;
  return <>{children}</>;
}
