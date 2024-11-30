import { ChampionsList } from "./components/champions-list";
import { HallOfFame } from "./components/hall-of-fame";

export default function LeagueHistoryPage() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">BTSH League History</h1>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <div className="grid gap-8 md:grid-cols-2">
          <ChampionsList />
          <HallOfFame />
        </div>
      </main>
    </div>
  );
}
