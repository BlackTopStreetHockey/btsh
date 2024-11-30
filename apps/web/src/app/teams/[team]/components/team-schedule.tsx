import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const scheduleData = [
  { date: "2023-10-11", opponent: "Vancouver Canucks", result: "W 5-3" },
  { date: "2023-10-14", opponent: "Calgary Flames", result: "L 3-4 (OT)" },
  { date: "2023-10-17", opponent: "Buffalo Sabres", result: "W 4-2" },
  { date: "2023-10-19", opponent: "New York Rangers", result: "W 3-1" },
  { date: "2023-10-21", opponent: "Winnipeg Jets", result: "W 4-3" },
]

export function TeamSchedule() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Games</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {scheduleData.map((game, index) => (
            <li key={index} className="flex justify-between items-center border-b pb-2 last:border-b-0">
              <div>
                <p className="font-semibold">{game.opponent}</p>
                <p className="text-sm text-gray-500">{game.date}</p>
              </div>
              <span className={`font-bold ${game.result.startsWith('W') ? 'text-green-600' : 'text-red-600'}`}>
                {game.result}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}

