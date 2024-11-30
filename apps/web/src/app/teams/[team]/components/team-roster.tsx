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
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { mockPlayers } from "@/data/__mocks__/players";

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

export function TeamRoster({ team }: { team: string }) {
  const [sortField, setSortField] = useState<SortField>("number");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  // Mock data - replace with actual data from API
  const players = mockPlayers.filter((player) => player.team == team);

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
      <ArrowUp
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
                <SortableHeader field="name">Name</SortableHeader>
              </TableHead>
              <TableHead>
                <SortableHeader field="number">#</SortableHeader>
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
                <SortableHeader field="assists">GAA</SortableHeader>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedPlayers.map((player) => (
              <TableRow key={player.name}>
                <TableCell>{player.name}</TableCell>
                <TableCell className="text-center">{player.number}</TableCell>
                <TableCell className="text-center">{player.position}</TableCell>
                <TableCell className={`text-center ${player.gender === "M" ? "text-blue-600" : "text-pink-600"}`}>{player.gender}</TableCell>
                <TableCell className="text-center">{player.gp}</TableCell>
                <TableCell className="text-center">{player.goals}</TableCell>
                <TableCell className="text-center">{(player.goals && player.gp? Math.round(player.goals / player.gp * 100) / 100 : 0)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
