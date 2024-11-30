"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"


const goalData = [
  { month: "Oct", goalsFor: 45, goalsAgainst: 30 },
  { month: "Nov", goalsFor: 52, goalsAgainst: 35 },
  { month: "Dec", goalsFor: 48, goalsAgainst: 40 },
  { month: "Jan", goalsFor: 55, goalsAgainst: 38 },
  { month: "Feb", goalsFor: 50, goalsAgainst: 32 },
]

const winLossData = [
  { month: "Oct", wins: 8, losses: 4 },
  { month: "Nov", wins: 10, losses: 3 },
  { month: "Dec", wins: 7, losses: 6 },
  { month: "Jan", wins: 11, losses: 2 },
  { month: "Feb", wins: 9, losses: 3 },
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
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
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
            <div className="flex flex-col items-center">
              <span className="text-2xl font-bold text-yellow-600">2.3</span>
              <span className="text-sm text-gray-500">GAA</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

