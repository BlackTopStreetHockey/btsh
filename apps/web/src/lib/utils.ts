import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Convert hex to RGB for contrast calculation
function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  // Remove the hash if present
  hex = hex.replace(/^#/, "");

  // Convert 3-digit hex to 6-digit
  if (hex.length === 3) {
    hex = hex
      .split("")
      .map((char) => char + char)
      .join("");
  }

  const result = /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

// Calculate relative luminance
function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

// Get contrasting color (black or white) based on background color
export function getContrastingColor(backgroundColor: string): string {
  // Default to black if color parsing fails
  if (!backgroundColor.startsWith("#")) {
    return "#000000";
  }

  const rgb = hexToRgb(backgroundColor);
  if (!rgb) return "#000000";

  const luminance = getLuminance(rgb.r, rgb.g, rgb.b);
  return luminance > 0.179 ? "#000000" : "#FFFFFF";
}
