"use client";
import { useGame } from "@/hooks/requests/useGame";
import { useParams } from "next/navigation";
import CompletedGame from "@/components/games/CompletedGame";
import { ScheduledGame } from "@/components/games/ScheduledGame";

export default function GamePage() {
  const { id } = useParams();
  const { game, placeholder } = useGame({ id });
  console.log(game);

  if (!!placeholder) return placeholder;
  const isCompleted = game.status === "completed";

  return isCompleted ? (
    <CompletedGame game={game} />
  ) : (
    <ScheduledGame game={game} />
  );
}
