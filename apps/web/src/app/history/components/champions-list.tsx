import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Trophy } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export const champions = [
  { year: 2024, team: "Fuzz", runner_up: "Mega Touch" },
  { year: 2023, team: "Lbs", runner_up: "Cobra Kai" },
  { year: 2022, team: "--" },
  { year: 2021, team: "Fuzz" },
  { year: 2019, team: "Fuzz" },
  { year: 2018, team: "Fuzz" },
  { year: 2017, team: "Fresh Kills" },
  { year: 2016, team: "Rehabs" },
  { year: 2015, team: "Filthier" },
  { year: 2014, team: "Fresh Kills" },
  { year: 2013, team: "Corlear's Hookers" },
  { year: 2012, team: "Lbs, Inc" },
  { year: 2011, team: "Fresh Kills" },
  { year: 2010, team: "Happy Little Elves" },
  { year: 2009, team: "Skyfighters" },
  { year: 2008, team: "Fresh Kills" },
  { year: 2007, team: "Dark Rainbows" },
  { year: 2006, team: "What The Puck" },
  { year: 2005, team: "Pork Fried Rice" },
  { year: 2004, team: "Lbs" },
  { year: 2003, team: "Skyfighters" },
  { year: 2003, team: "Lbs" },
  { year: 2002, team: "Rehabs" },
  { year: 2002, team: "What The Puck" },
  { year: 2001, team: "Rumpshakers" },
  { year: 2001, team: "Rehabs" },
  { year: 2000, team: "Funny Garbage" },
];

export function ChampionsList() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex gap-2 items-center"><Trophy />League Champions</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Year</TableHead>
              <TableHead>Team</TableHead>
              <TableHead>Runner Up</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {champions.map((champion) => (
              <TableRow key={champion.year}>
                <TableCell>{champion.year}</TableCell>
                <TableCell>{champion.team}</TableCell>
                <TableCell>{champion.runner_up || "--"}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
