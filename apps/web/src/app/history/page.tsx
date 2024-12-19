import { ChampionsList } from "./components/champions-list";
import { HallOfFame } from "./components/hall-of-fame";

export default function LeagueHistoryPage() {
  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">BTSH League History</h1>
        <div className="grid gap-8 md:grid-cols-2">
          <ChampionsList />
          <HallOfFame />
        </div>
      </main>
    </div>
  );
}
