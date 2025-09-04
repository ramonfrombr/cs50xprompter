"use client";
import { useState, useContext, useEffect } from "react";
import { AuthContext } from "@/app/components/AuthContext";
import { useRouter } from "next/navigation";
import { apiUrl } from "@/app/apiUrl";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, token, loading } = useContext(AuthContext);
  const router = useRouter();

  useEffect(() => {
    if (!loading && token) {
      router.replace("/teleprompter");
    }
  }, [token, loading, router]);

  const handleLogin = async () => {
    const res = await fetch(`${apiUrl}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (res.ok) {
      login(data.token);
      router.push("/teleprompter");
    } else {
      alert(data.error);
    }
  };

  if (loading || token) return <p>Loading...</p>;

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl mb-4">Login</h1>
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        type="text"
        className="border p-2 mb-2"
      />
      <input
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        className="border p-2 mb-2"
      />
      <button
        className="bg-blue-500 text-white px-4 py-2"
        onClick={handleLogin}
      >
        Login
      </button>
    </div>
  );
}
