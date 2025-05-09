"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

// Mock data for course performance
const data = [
  {
    name: "CS101",
    average: 3.2,
  },
  {
    name: "CS108",
    average: 3.5,
  },
  {
    name: "CS201",
    average: 2.8,
  },
]

export function Overview() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          domain={[0, 4]}
          ticks={[0, 1, 2, 3, 4]}
          tickFormatter={(value) => `${value}`}
        />
        <Tooltip formatter={(value) => [`${value}`, "Average Grade"]} labelFormatter={(label) => `Course: ${label}`} />
        <Bar dataKey="average" fill="#f97316" radius={[4, 4, 0, 0]} className="fill-primary" />
      </BarChart>
    </ResponsiveContainer>
  )
}
