"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const goalData = [
  { month: "Mar", goalsFor: 22, goalsAgainst: 15 },
  { month: "Apr", goalsFor: 25, goalsAgainst: 17 },
  { month: "May", goalsFor: 28, goalsAgainst: 20 },
  { month: "Jun", goalsFor: 32, goalsAgainst: 22 },
  { month: "Jul", goalsFor: 35, goalsAgainst: 25 },
  { month: "Aug", goalsFor: 14, goalsAgainst: 18 },
  { month: "Sep", goalsFor: 2, goalsAgainst: 4 },
  { month: "Oct", goalsFor: 0, goalsAgainst: 0 },
]

const winLossData = [
  { month: "Mar", wins: 2, losses: 2 },
  { month: "Apr", wins: 4, losses: 0 },
  { month: "May", wins: 3, losses: 1 },
  { month: "Jun", wins: 3, losses: 1 },
  { month: "Jul", wins: 1, losses: 3 },
  { month: "Aug", wins: 2, losses: 2 },
  { month: "Sep", wins: 1, losses: 1 },
  { month: "Oct", wins: 0, losses: 0 },
]

export function TeamPerformance() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Goal Performance</CardTitle>
          <CardDescription>Monthly goals for and against</CardDescription>
        </CardHeader>
        <CardContent className="pt-2">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={goalData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="goalsFor" name="Goals For" fill="#2563eb" />
              <Bar dataKey="goalsAgainst" name="Goals Against" fill="#dc2626" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Win/Loss Record</CardTitle>
          <CardDescription>Monthly wins and losses</CardDescription>
        </CardHeader>
        <CardContent className="pt-2">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={winLossData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="wins" name="Wins" stroke="#2563eb" strokeWidth={2} />
              <Line type="monotone" dataKey="losses" name="Losses" stroke="#dc2626" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>Team Statistics</CardTitle>
          <CardDescription>Key performance indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            <div className="flex flex-col items-center">
              <span className="text-2xl font-bold text-blue-600">3.5</span>
              <span className="text-sm text-gray-500">Goals/Game</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-2xl font-bold text-red-600">2.8</span>
              <span className="text-sm text-gray-500">GA/Game</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-2xl font-bold text-green-600">54.5%</span>
              <span className="text-sm text-gray-500">Shootout %</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

