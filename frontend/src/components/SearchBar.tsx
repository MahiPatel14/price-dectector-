"use client";
import { Search } from "lucide-react";

interface Props {
  value: string;
  onChange: (v: string) => void;
  onSearch: () => void;
  loading: boolean;
}

export default function SearchBar({ value, onChange, onSearch, loading }: Props) {
  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !loading) onSearch();
  };

  return (
    <div className="search-section">
      <div className="search-form">
        <div className="search-input-wrap">
          <Search size={18} />
          <input
            id="product-search"
            className="search-input"
            type="text"
            placeholder="Search a product (e.g. iPhone 15, Samsung TV…)"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKey}
            disabled={loading}
            autoComplete="off"
          />
        </div>
        <button
          id="search-btn"
          className="search-btn"
          onClick={onSearch}
          disabled={loading || !value.trim()}
        >
          {loading ? (
            <>
              <span className="spinner" />
              Searching…
            </>
          ) : (
            <>
              <Search size={16} />
              Search
            </>
          )}
        </button>
      </div>
    </div>
  );
}
