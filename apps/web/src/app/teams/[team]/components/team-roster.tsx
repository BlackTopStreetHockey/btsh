"use client";

import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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

import { useRoster } from "@/hooks/requests/useRoster";
import { useSeasons } from "@/hooks/requests/useSeasons";

type SortField = "name" | "position" | "gender" | "gp" | "goals" | "gpg";
type SortDirection = "asc" | "desc";

export function TeamRoster({
  seasonId,
  teamId,
}: {
  seasonId: string;
  teamId: string;
}) {
  const [sortField, setSortField] = useState<SortField>("name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const { roster } = useRoster({ seasonId, teamId });
  const { seasons } = useSeasons({});

  console.log("seasons:", seasons);

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
          <CardTitle>Roster</CardTitle>
          <div className="w-32">
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select Season" />
              </SelectTrigger>
              <SelectContent>
                {seasons?.map((season) => (
                  <SelectItem
                    key={season.id}
                    value={season.id.toString()}
                    defaultChecked={season.is_current}
                  >
                    {season.year}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
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
                <SortableHeader field="gpg">GPG</SortableHeader>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedPlayers.map((player) => (
              <TableRow key={player.user.id}>
                <TableCell>{player.user.full_name}</TableCell>
                <TableCell className="text-center uppercase text-xs">
                  {player.is_captain ? "⭐️ " : ""}{" "}
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
      </CardContent>
    </Card>
  );
}
