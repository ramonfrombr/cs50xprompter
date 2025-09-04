"use client";

import { useEffect } from "react";
import ProtectedRoute from "../components/ProtectedRoute";
import useSocket from "../hooks/useSocket";

export default function Teleprompter() {
  const { socket, connected } = useSocket();

  useEffect(() => {
    if (!socket) return;

    socket.on("message", (data) => {
      console.log("Server says: ", data);
    });

    return () => {
      socket.disconnect();
    };
  }, [socket]);

  return (
    <ProtectedRoute>
      <h1>Teleprompter</h1>
      <p>{connected ? "Connected to server" : "Connecting..."}</p>
    </ProtectedRoute>
  );
}
