"use client";

import * as React from "react";

import {
  BarChart,
  BookOpenText,
  Calendar,
  Clock,
  GithubIcon,
  Settings2,
  Speech,
  Table,
  Users,
  LifeBuoy,
  Send,
} from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { CreditCard, LogOut, PlusCircle, Settings, User } from 'lucide-react'

import BTSHLogo from "@/components/navigation/btsh-logo";

import { SeasonSelector } from "@/components/season-selector";

const data = {
  user: {
    name: "Justin",
    email: "justin@btsh.org",
    avatar: "/teams/what_the_puck.jpg",
  },
  pages: [
    {
      title: "Schedule",
      url: "/league-schedule",
      icon: Calendar,
    },
    {
      title: "Standings",
      url: "/standings",
      icon: Table,
    },
    {
      title: "Teams",
      url: "/teams",
      icon: Users,
    },
    {
      title: "Stats",
      url: "/stats",
      icon: BarChart,
    },
    {
      title: "Rules",
      url: "/rules",
      icon: BookOpenText,
    },
    {
      title: "History",
      url: "/history",
      icon: Clock,
    },
  ],
  navSecret: [
    {
      title: "Ref",
      url: "/ref",
      icon: Speech,
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings2,
    },
  ],
  navSecondary: [
    {
      title: "Contribute",
      url: "https://github.com/blacktopstreethockey/btsh",
      icon: GithubIcon,
    },
    {
      title: "Support",
      url: "#",
      icon: LifeBuoy,
    },
    {
      title: "Feedback",
      url: "#",
      icon: Send,
    },
  ],
};

export function AppNavbar({ ...props }) {
  return (
    <div className="sticky top-0 z-40 w-full backdrop-blur flex-none transition-colors duration-500 lg:z-50 lg:border-b lg:border-slate-900/10 dark:border-slate-50/[0.06] bg-white supports-backdrop-blur:bg-white/95 dark:bg-slate-900/75">
      <div className="flex w-full items-center space-between">
        <BTSHLogo />
        <SeasonSelector />

        <div className="flex grow items-center gap-1 px-1">
          {data.pages.map((page) => (
            <Button key={page.title} variant="ghost" className={`${page.title === "Standings" ? "bg-blue-500 text-white" : ""}`}>
              <page.icon className="w-4 h-4" />
              {page.title}
            </Button>
          ))}
        </div>

        <div className="flex items-center gap-1 px-1">

        <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                <Avatar className="h-10 w-10">
                  <AvatarImage src="/placeholder.svg" alt="User avatar" />
                  <AvatarFallback>JD</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="start" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">John Doe</p>
                  <p className="text-xs leading-none text-muted-foreground">john@example.com</p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem>
                  <User className="mr-2 h-4 w-4" />
                  <span>Profile</span>
                  <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Settings className="mr-2 h-4 w-4" />
                  <span>Settings</span>
                  <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
                <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          </div>
      </div>
    </div>
  );
}
