"use client";
import { Lightbulb } from "lucide-react";

interface Props {
  decision: string | null;
  trend: string | null;
}

type BannerType = "buy" | "wait" | "stable";

function classify(decision: string | null): BannerType {
  if (!decision) return "stable";
  const lower = decision.toLowerCase();
  if (lower.includes("buy")) return "buy";
  if (lower.includes("wait")) return "wait";
  return "stable";
}

const CONFIG: Record<BannerType, { icon: string; title: string }> = {
  buy:    { icon: "🟢", title: "Buy Now!" },
  wait:   { icon: "🟡", title: "Hold On" },
  stable: { icon: "🔵", title: "Price Stable" },
};

export default function Recommendation({ decision, trend }: Props) {
  const type = classify(decision);
  const { icon, title } = CONFIG[type];

  return (
    <div className="section">
      <div className="card">
        <div className="card-title">
          <Lightbulb size={15} />
          Recommendation
        </div>

        <div className={`rec-banner ${type}`}>
          <div className="rec-icon">{icon}</div>
          <div>
            <div className="rec-title">{title}</div>
            <div className="rec-desc">
              {decision ?? "Not enough history to make a recommendation yet."}
            </div>
            {trend && (
              <div className="rec-desc" style={{ marginTop: 6 }}>
                {trend}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
