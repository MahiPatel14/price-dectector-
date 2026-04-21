"use client";
import { ShoppingBag } from "lucide-react";

const SITE_EMOJI: Record<string, string> = {
  Flipkart: "🟡",
  Croma: "🔵",
};

interface Props {
  prices: Record<string, number>;
  bestSite: string;
}

export default function PriceCards({ prices, bestSite }: Props) {
  return (
    <div className="section">
      <div className="card">
        <div className="card-title">
          <ShoppingBag size={15} />
          Live Prices Across Websites
        </div>
        <div className="price-grid">
          {Object.entries(prices).map(([site, price]) => (
            <div
              key={site}
              className={`price-card ${site === bestSite ? "best" : ""}`}
            >
              <div className="price-card-site">
                {SITE_EMOJI[site] ?? "🛒"} {site}
              </div>
              <div className="price-card-value">
                <span>₹</span>
                {price.toLocaleString("en-IN")}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
