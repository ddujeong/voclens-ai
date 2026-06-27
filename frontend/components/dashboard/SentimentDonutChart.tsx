"use client";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";

type Sentiment = {
    sentiment: string;
    count: number;
    rate: number;
};

const COLORS = [
    "#22c55e",
    "#ef4444",
    "#94a3b8",
];

export default function SentimentDonutChart({
    data,
}: {
    data: Sentiment[];
}) {
    return (
        <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={data}
                        dataKey="count"
                        nameKey="sentiment"
                        innerRadius={70}
                        outerRadius={110}
                        label={({ percent }) =>
                            `${((percent ?? 0) * 100).toFixed(1)}%`
                        }
                    >
                        {data.map((_, index) => (
                            <Cell
                                key={index}
                                fill={COLORS[index % COLORS.length]}
                            />
                        ))}
                    </Pie>

                    <Tooltip />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}