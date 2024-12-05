import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
const scheduleData = [
  { date: "2023-10-11", opponent: "Gouging Anklebiters", result: "W 5-3" },
  { date: "2023-10-14", opponent: "Cobra Kai", result: "L 3-4 (OT)" },
  { date: "2023-10-17", opponent: "Butchers", result: "W 4-2" },
  { date: "2023-10-19", opponent: "Mega Touch", result: "W 3-1" },
  { date: "2023-10-21", opponent: "What the Puck", result: "W 4-3" },
];

export function TeamSchedule({
  seasonId,
  teamId,
  seasonYear,
}: {
  seasonId: string;
  teamId: string;
  seasonYear: string;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{seasonYear} Schedule</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {scheduleData.map((game, index) => (
            <li
              key={index}
              className="flex justify-between items-center border-b pb-2 last:border-b-0"
            >
              <div className="flex items-center space-x-2">
                <Image
                  src="/teams/btsh.jpg"
                  alt={game.opponent}
                  width={30}
                  height={30}
                />
                <div>
                  <p className="font-semibold">{game.opponent}</p>
                  <p className="text-xs text-gray-500">{game.date}</p>
                </div>
              </div>

              <span
                className={`font-bold ${
                  game.result.startsWith("W")
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                {game.result}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
