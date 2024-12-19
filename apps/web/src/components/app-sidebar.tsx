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

import BTSHLogo from "@/components/navigation/btsh-logo";
import { NavPages } from "./navigation/nav-pages";
import { NavSecondary } from "@/components/navigation/nav-secondary";
import { NavUser } from "@/components/navigation/nav-user";
import { SeasonSelector } from "@/components/season-selector";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";

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

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <div className="flex items-center justify-between">
          <BTSHLogo />
          <SeasonSelector />
        </div>
      </SidebarHeader>
      <SidebarContent>
        <NavPages items={data.pages} />
      </SidebarContent>
      <SidebarFooter>
        <NavSecondary items={data.navSecondary} />
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
