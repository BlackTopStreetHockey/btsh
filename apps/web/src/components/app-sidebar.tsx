"use client";

import * as React from "react";
import { BarChart, Calendar, Settings2, Table, Users } from "lucide-react";

import BTSHLogo from "@/components/navigation/btsh-logo";
import { NavPages } from "./navigation/nav-pages";
import { NavUser } from "@/components/navigation/nav-user";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";

// This is sample data.
const data = {
  user: {
    name: "Justin",
    email: "justin@btsh.org",
    avatar: "/avatars/shadcn.jpg",
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
      title: "Settings",
      url: "/settings",
      icon: Settings2,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <BTSHLogo />
      </SidebarHeader>
      <SidebarContent>
        <NavPages items={data.pages} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
