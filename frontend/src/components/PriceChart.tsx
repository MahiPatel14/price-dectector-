"use client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { AreaChart as AreaIcon } from "lucide-react";
import type { HistoryRow } from "@/lib/api";

interface Props {
  rows: HistoryRow[];
}

const COLORS: Record<string, string> = {
  Flipkart: "#f6e05e",
  Croma:    "#63b3ed",
};

function formatDate(dateStr: string) {
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-IN", { month: "short", day: "numeric" });
  } catch {
    return dateStr.slice(0, 10);
  }
}

export default function PriceChart({ rows }: Props) {
  if (!rows.length) return null;

  // Build per-date points: { date: string, [site]: number }
  type ChartPoint = { date: string } & Record<string, number | string>;
  const map = new Map<string, ChartPoint>();
  rows.forEach((r) => {
    const key = formatDate(r.date);
    if (!map.has(key)) map.set(key, { date: key });
    map.get(key)![r.source] = r.price;
  });
  const data = Array.from(map.values());

  const sources = Array.from(new Set(rows.map((r) => r.source)));

  return (
    <div className="section">
      <div className="card">
        <div className="card-title">
          <AreaIcon size={15} />
          Price History
        </div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis
                dataKey="date"
                tick={{ fill: "#64748b", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: "#64748b", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
                width={48}
              />
              <Tooltip
                contentStyle={{
                  background: "#0d1628",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: 10,
                  fontSize: 13,
                  color: "#f0f4ff",
                }}
                formatter={(v) => [`₹${Number(v).toLocaleString("en-IN")}`, ""]}
              />
              <Legend
                wrapperStyle={{ fontSize: 12, color: "#64748b", paddingTop: 8 }}
              />
              {sources.map((src) => (
                <Line
                  key={src}
                  type="monotone"
                  dataKey={src}
                  stroke={COLORS[src] ?? "#9f7aea"}
                  strokeWidth={2}
                  dot={{ r: 3, fill: COLORS[src] ?? "#9f7aea" }}
                  activeDot={{ r: 5 }}
                  connectNulls
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
