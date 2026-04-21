"use client";
import { TableProperties } from "lucide-react";
import type { HistoryRow } from "@/lib/api";

interface Props {
  rows: HistoryRow[];
}

function formatDate(dateStr: string) {
  try {
    return new Date(dateStr).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return dateStr;
  }
}

export default function RawDataTable({ rows }: Props) {
  if (!rows.length) return null;

  // show most recent 50 rows
  const display = [...rows].reverse().slice(0, 50);

  return (
    <div className="section">
      <div className="card">
        <div className="card-title">
          <TableProperties size={15} />
          Raw Data ({rows.length} records)
        </div>
        <div className="data-table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Date / Time</th>
                <th>Source</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {display.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ color: "var(--text-muted)", fontSize: 11 }}>
                    {rows.length - idx}
                  </td>
                  <td>{formatDate(row.date)}</td>
                  <td>{row.source}</td>
                  <td style={{ color: "var(--text-primary)", fontWeight: 600 }}>
                    ₹{row.price.toLocaleString("en-IN")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
