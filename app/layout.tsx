import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Project Genesis — An artificial life",
  description: "Observe an artificial organism whose decisions are constrained by a simulation of the real 302-neuron C. elegans connectome.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
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
