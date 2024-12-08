import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import BTSHNavbar from "@/components/navigation/btsh-navbar";
import clsx from "clsx";

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
  // get the width of window
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div>
          <BTSHNavbar />
          {/* tailwind class to push content to the right on lg screens and push down on small screens and xs screens */}
          <div className="min-h-screen mt-16 md:mt-0 ml-0 md:ml-32">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
