import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"

const inductees = [
  { year: 2023, name: "Henrik Lundqvist", position: "Goalie" },
  { year: 2022, name: "Daniel Sedin", position: "Left Wing" },
  { year: 2022, name: "Henrik Sedin", position: "Center" },
  { year: 2021, name: "Jarome Iginla", position: "Right Wing" },
  // ... add more inductees here
  { year: 1999, name: "Wayne Gretzky", position: "Center" },
]

export function HallOfFame() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Hall of Fame Inductees</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px] pr-4">
          {inductees.map((inductee, index) => (
            <div key={index} className="mb-4 last:mb-0">
              <h3 className="text-lg font-semibold">{inductee.name}</h3>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant="secondary">{inductee.year}</Badge>
                <span className="text-sm text-gray-500">{inductee.position}</span>
              </div>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}

