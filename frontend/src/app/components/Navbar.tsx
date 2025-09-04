"use client";
import { useContext } from "react";
import { AuthContext } from "./AuthContext";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { token, logout, loading } = useContext(AuthContext);
  const router = useRouter();

  if (loading) {
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  return (
    <nav className="flex items-center justify-between bg-gray-800 text-white px-4 py-2">
      <div className="text-xl font-bold">
        <Link href="/">CS50xPrompter</Link>
      </div>

      <div className="space-x-4">
        {!token ? (
          <>
            <Link href="/auth/login">
              <button className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded">
                Login
              </button>
            </Link>
            <Link href="/auth/register">
              <button className="bg-green-500 hover:bg-blue-600 px-3 py-1 rounded">
                Register
              </button>
            </Link>
          </>
        ) : (
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
