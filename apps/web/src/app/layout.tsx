import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

import { AppNavbar } from "@/components/app-navbar";
import { Toaster } from "@/components/ui/toaster";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "BTSH",
  description: "Black Top Street Hockey",
};

export default function BTSHLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex flex-col min-h-screen">
          <AppNavbar />
          <main className="bg-gray-100">
            {children}
            <Toaster />
          </main>
        </div>
      </body>
    </html>
  );
}
