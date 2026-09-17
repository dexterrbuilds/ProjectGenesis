import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Project Genesis — An artificial life",
  description: "Experiment 001. An artificial life, in progress. The beginning is approaching.",
  icons: {
    icon: "/genesis-logo.png",
    shortcut: "/genesis-logo.png",
    apple: "/genesis-logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
