"use client";

import React from "react";
import { Button } from "@/components/ui/button";

import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

import { teams } from "@/data/teams";

export default function GameDetails({
  date,
  setDate,
  homeTeam,
  awayTeam,
  setHomeTeam,
  setAwayTeam,
}: {
  date: Date;
  setDate: (date: Date) => void;
  homeTeam: Team;
  awayTeam: Team;
  setHomeTeam: (team: Team) => void;
  setAwayTeam: (team: Team) => void;
}) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Open</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Edit Game Details</SheetTitle>
          <SheetDescription>
            Make changes to the game details here. Click save when you're done.
          </SheetDescription>
        </SheetHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="ref1" className="text-right">
              String Referee
            </Label>
            <Input id="ref1" value="Alex M" className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="ref2" className="text-right">
              Fence Referee
            </Label>
            <Input id="ref2" value="Zac H" className="col-span-3" />
          </div>

          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="time" className="text-right">
              Game Time
            </Label>
            <Input id="time" value="12:00PM" className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="awayTeam" className="text-right">
              Away Team
            </Label>
            <div className="col-span-3">
              <Select
                defaultValue={teams[10].shortName}
                onValueChange={(value) => {
                  const foundTeam = teams.find((t) => t.shortName === value);
                  if (foundTeam) {
                    setAwayTeam(foundTeam as Team);
                  }
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select team" />
                </SelectTrigger>
                <SelectContent>
                  {teams.map((team) => (
                    <SelectItem key={team.shortName} value={team.shortName}>
                      {team.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="homeTeam" className="text-right">
              Home Team
            </Label>
            <div className="col-span-3">
              <Select
                defaultValue={teams[9].shortName}
                onValueChange={(value) => {
                  const foundTeam = teams.find((t) => t.shortName === value);
                  if (foundTeam) {
                    setHomeTeam(foundTeam as Team);
                  }
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select team" />
                </SelectTrigger>
                <SelectContent>
                  {teams.map((team) => (
                    <SelectItem key={team.shortName} value={team.shortName}>
                      {team.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <Label htmlFor="date" className="text-left">
            Date
          </Label>
          <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            className="flex rounded-md border justify-center items-center"
          />
        </div>
        <SheetFooter>
          <SheetClose asChild>
            <Button type="submit">Save</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}