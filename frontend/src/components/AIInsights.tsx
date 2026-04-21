"use client";
import { BrainCircuit, TrendingUp, TrendingDown, Minus } from "lucide-react";

interface Props {
  currentPrice: number;
  prediction: number | null;
}

export default function AIInsights({ currentPrice, prediction }: Props) {
  const delta =
    prediction !== null ? prediction - currentPrice : null;
  const pct =
    delta !== null && currentPrice > 0
      ? ((delta / currentPrice) * 100).toFixed(1)
      : null;

  const direction =
    delta === null ? "same" : delta > 0 ? "up" : delta < 0 ? "down" : "same";

  const DeltaIcon =
    direction === "up"
      ? TrendingUp
      : direction === "down"
      ? TrendingDown
      : Minus;

  return (
    <div className="section">
      <div className="card">
        <div className="card-title">
          <BrainCircuit size={15} />
          AI Insights
        </div>
        <div className="metrics-grid">
          {/* Current price */}
          <div className="metric-card">
            <div className="metric-label">Current Best Price</div>
            <div className="metric-value">
              <span>₹</span>
              {currentPrice.toLocaleString("en-IN")}
            </div>
            <div className="metric-delta same">Live price now</div>
          </div>

          {/* Predicted price */}
          <div className="metric-card">
            <div className="metric-label">AI Predicted Price</div>
            {prediction !== null ? (
              <>
                <div className="metric-value">
                  <span>₹</span>
                  {prediction.toLocaleString("en-IN")}
                </div>
                <div className={`metric-delta ${direction}`}>
                  <DeltaIcon size={12} />
                  {direction === "same"
                    ? "Stable"
                    : `${direction === "up" ? "+" : ""}${pct}% vs current`}
                </div>
              </>
            ) : (
              <>
                <div className="metric-value" style={{ fontSize: "1.3rem", color: "var(--text-muted)" }}>
                  Not enough data
                </div>
                <div className="metric-delta same">Need more history</div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
