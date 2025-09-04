import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

export default function useSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Detect if we are in browser
    if (typeof window === "undefined") return;

    // Use backend service name in Docker, fallback to localhost for dev
    const backendUrl =
      window.location.hostname === "localhost"
        ? "http://localhost:5000"
        : `${process.env.NEXT_PUBLIC_API_URL}`;
    const token = localStorage.getItem("token");

    const s = io(backendUrl, {
      query: { token },
      transports: ["websocket"],
    });

    s.on("connect", () => setConnected(true));
    s.on("disconnect", () => setConnected(false));

    setSocket(s);

    return () => {
      s.disconnect();
    };
  }, []);

  return { socket, connected };
}
