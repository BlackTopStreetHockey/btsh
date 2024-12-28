"use client";
import { useGame } from "@/hooks/requests/useGame";
import { useParams } from "next/navigation";
import ScheduledGame from "./components/ScheduledGame";
import CompletedGame from "./components/CompletedGame";

export default function GamePage() {
  const { id } = useParams();
  const { game, placeholder } = useGame({ id });

  if (!!placeholder) return placeholder;
  const isCompleted = game.status === "completed";

  return isCompleted ? (
    <CompletedGame game={game} />
  ) : (
    <ScheduledGame game={game} />
  );
}
