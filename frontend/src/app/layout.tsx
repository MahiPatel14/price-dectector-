import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Price Watch AI — Smart Price Tracking & Prediction",
  description:
    "Track live prices across Flipkart and Croma, get AI-powered price predictions, and buy at the right time.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>{children}</body>
    </html>
  );
}
