"use client";

import { useState } from "react";

import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUp, Star } from "lucide-react";
import { Button } from "@/components/ui/button";

import { useRoster } from "@/hooks/requests/useRoster";

type SortField = "full_name" | "position" | "gender" | "gp" | "goals" | "gpg";
type SortDirection = "asc" | "desc";

export function TeamRoster({
  seasonId,
  teamId,
  seasonYear,
}: {
  seasonId: string;
  teamId: string;
  seasonYear: string;
}) {
  const [sortField, setSortField] = useState<SortField>("full_name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");
  const { roster } = useRoster({ seasonId, teamId });

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const sortedPlayers = roster
    ? [...roster].sort((a, b) => {
        const multiplier = sortDirection === "asc" ? 1 : -1;

        if (typeof a[sortField] === "string") {
          return (
            multiplier *
            (a[sortField] as string).localeCompare(b[sortField] as string)
          );
        }

        return (
          multiplier * ((a[sortField] as number) - (b[sortField] as number))
        );
      })
    : [];

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
        <div className="flex justify-between items-center">
          <CardTitle>{seasonYear} Roster</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[500px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[150px]">
                  <SortableHeader field="full_name">Name</SortableHeader>
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
                  <SortableHeader field="gpg">GPG</SortableHeader>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedPlayers.map((player) => (
                <TableRow key={player.user.id}>
                  <TableCell className="flex w-[150px] items-center gap-1">
                    {player.user.full_name}
                    {player.is_captain ? (
                      <Star size={16} className="text-yellow-500" />
                    ) : (
                      ""
                    )}
                  </TableCell>
                  <TableCell className="text-center uppercase text-xs">
                    {player.position.substring(0, 1)}
                  </TableCell>
                  <TableCell
                    className={`text-center ${player.user.gender === "male" ? "text-blue-600" : "text-pink-600"}`}
                  >
                    {player.user.gender === "male" ? "M" : "F"}
                  </TableCell>
                  <TableCell className="text-center">{player.gp}</TableCell>
                  <TableCell className="text-center">{player.goals}</TableCell>
                  <TableCell className="text-center">
                    {player.goals && player.gp
                      ? Math.round((player.goals / player.gp) * 100) / 100
                      : 0}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
