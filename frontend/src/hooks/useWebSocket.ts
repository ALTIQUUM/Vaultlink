import { useEffect } from "react";
import { WS_BASE_URL } from "../utils/constants";

export function useWebSocket(userId: number | null, onMessage: (payload: unknown) => void) {
  useEffect(() => {
    if (!userId) return undefined;
    const socket = new WebSocket(`${WS_BASE_URL}/ws/notifications/${userId}`);
    socket.onmessage = (event) => onMessage(JSON.parse(event.data) as unknown);
    return () => socket.close();
  }, [onMessage, userId]);
}
