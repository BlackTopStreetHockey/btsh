"use client";

import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";

type SortField =
  | "number"
  | "name"
  | "position"
  | "gender"
  | "gp"
  | "goals"
  | "assists"
  | "points";
type SortDirection = "asc" | "desc";

export function TeamRoster() {
  const [sortField, setSortField] = useState<SortField>("number");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  // Mock data - replace with actual data from API
  const players: Player[] = [
    {
      number: 97,
      name: "Connor McDavid",
      gender: "M",
      position: "F",
      gp: 78,
      goals: 64,
      assists: 89,
      points: 153,
    },
    {
      number: 29,
      name: "Leon Draisaitl",
      gender: "M",
      position: "F",
      gp: 78,
      goals: 52,
      assists: 76,
      points: 128,
    },
    {
      number: 93,
      name: "Ryan Nugent-Hopkins",
      gender: "M",
      position: "F",
      gp: 78,
      goals: 37,
      assists: 67,
      points: 104,
    },
    {
      number: 25,
      name: "Darnell Nurse",
      gender: "M",
      position: "D",
      gp: 78,
      goals: 12,
      assists: 31,
      points: 43,
    },
    {
      number: 22,
      name: "Tyson Barrie",
      gender: "M",
      position: "D",
      gp: 78,
      goals: 13,
      assists: 42,
      points: 55,
    },
    {
      number: 19,
      name: "Kailer Yamamoto",
      gender: "W",
      position: "F",
      gp: 78,
      goals: 26,
      assists: 36,
      points: 62,
    },
    {
      number: 14,
      name: "Jesse Puljujarvi",
      gender: "W",
      position: "D",
      gp: 78,
      goals: 22,
      assists: 28,
      points: 50,
    },
    {
      number: 17,
      name: "Zach Hyman",
      gender: "W",
      position: "W",
      gp: 78,
      goals: 21,
      assists: 25,
      points: 46,
    },
    {
      number: 13,
      name: "Hendrix Lundvist",
      gender: "M",
      position: "G",
      gp: 78,
      goals: 20,
      assists: 23,
      points: 43,
    },
  ];

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const sortedPlayers = [...players].sort((a, b) => {
    const multiplier = sortDirection === "asc" ? 1 : -1;

    if (typeof a[sortField] === "string") {
      return (
        multiplier *
        (a[sortField] as string).localeCompare(b[sortField] as string)
      );
    }

    return multiplier * ((a[sortField] as number) - (b[sortField] as number));
  });

  const SortableHeader = ({
    field,
    children,
  }: {
    field: SortField;
    children: React.ReactNode;
  }) => (
    <Button
      variant="ghost"
      onClick={() => handleSort(field)}
      className="h-8 flex items-center gap-1"
    >
      {children}
      <ArrowUpDown
        size={16}
        className={`
        transition-transform
        ${sortField === field && sortDirection === "desc" ? "rotate-180" : ""}
        ${sortField === field ? "opacity-100" : "opacity-0"}
      `}
      />
    </Button>
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Roster</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <SortableHeader field="number">#</SortableHeader>
              </TableHead>
              <TableHead>
                <SortableHeader field="name">Name</SortableHeader>
              </TableHead>
              <TableHead>
                <SortableHeader field="position">Position</SortableHeader>
              </TableHead>
              <TableHead>
                <SortableHeader field="gender">Gender</SortableHeader>
              </TableHead>
              <TableHead>
                <SortableHeader field="gp">GP</SortableHeader>
              </TableHead>
              <TableHead className="text-right">
                <SortableHeader field="goals">Goals</SortableHeader>
              </TableHead>
              <TableHead className="text-right">
                <SortableHeader field="assists">Assists</SortableHeader>
              </TableHead>
              <TableHead className="text-right">
                <SortableHeader field="points">Points</SortableHeader>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedPlayers.map((player) => (
              <TableRow key={player.number}>
                <TableCell className="text-center">{player.number}</TableCell>
                <TableCell>{player.name}</TableCell>
                <TableCell className="text-center">{player.position}</TableCell>
                <TableCell className="text-center">{player.gender}</TableCell>
                <TableCell className="text-center">{player.gp}</TableCell>
                <TableCell className="text-center">{player.goals}</TableCell>
                <TableCell className="text-center">{player.assists}</TableCell>
                <TableCell className="text-center">{player.points}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
