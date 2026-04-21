"use client";

import { useState, useEffect } from "react";
import { Activity } from "lucide-react";

import SearchBar      from "@/components/SearchBar";
import PriceCards     from "@/components/PriceCards";
import AIInsights     from "@/components/AIInsights";
import Recommendation from "@/components/Recommendation";
import PriceChart     from "@/components/PriceChart";
import RawDataTable   from "@/components/RawDataTable";

import { searchProduct, fetchHistory } from "@/lib/api";
import type { SearchResult, HistoryRow } from "@/lib/api";

export default function HomePage() {
  const [query,    setQuery]    = useState("");
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState<string | null>(null);
  const [result,   setResult]   = useState<SearchResult | null>(null);
  const [history,  setHistory]  = useState<HistoryRow[]>([]);

  // We no longer load history on mount because history is tied to specific products.

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await searchProduct(query.trim());
      setResult(data);

      // Refresh history after new data saved
      const h = await fetchHistory(query.trim());
      setHistory(h.rows);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page-wrapper">
      {/* ── Header ─────────────────────────────────── */}
      <header className="header">
        <div className="header-badge">
          <Activity size={12} />
          AI-powered
        </div>
        <h1>Price Watch AI</h1>
        <p>
          Track live prices across Flipkart &amp; Croma, get smart predictions,
          and never overpay again.
        </p>
      </header>

      {/* ── Search ─────────────────────────────────── */}
      <SearchBar
        value={query}
        onChange={setQuery}
        onSearch={handleSearch}
        loading={loading}
      />

      {/* ── Error ──────────────────────────────────── */}
      {error && (
        <div className="banner banner-error" role="alert">
          ⚠️ {error}
        </div>
      )}

      {/* ── Anomalies Alert (Interactive) ──────────── */}
      {result?.anomalies && Object.keys(result.anomalies).length > 0 && (
        <div className="banner" style={{ backgroundColor: "rgba(255, 170, 0, 0.15)", color: "#ffb84d", borderColor: "rgba(255, 170, 0, 0.3)" }} role="alert">
          <strong>⚠️ Anomaly Prevented:</strong> Safely ignored prices from{" "}
          {Object.entries(result.anomalies).map(([site, price]) => `${site} (₹${price.toLocaleString()})`).join(", ")}
          {" "}as they statistically appear to be accessories rather than the requested product.
        </div>
      )}

      {/* ── Results (appear after search) ──────────── */}
      {result && (
        <>
          <PriceCards
            prices={result.prices}
            bestSite={result.best_site}
          />

          <AIInsights
            currentPrice={result.best_value}
            prediction={result.prediction}
          />

          <Recommendation
            decision={result.decision}
            trend={result.trend}
          />
        </>
      )}

      {/* ── Chart & Table (shown if history exists) ─ */}
      {history.length > 0 && (
        <>
          <PriceChart rows={history} />
          <RawDataTable rows={history} />
        </>
      )}

      {/* ── Empty state ─────────────────────────────── */}
      {!result && !loading && history.length === 0 && (
        <div className="banner banner-info">
          🔍 Search for any product above to start tracking prices and get AI
          predictions.
        </div>
      )}
    </main>
  );
}
