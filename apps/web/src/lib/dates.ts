import { formatDate } from "date-fns";

export default function formatDateNoTimezone(
  date: string | number | Date,
  formatStr: string, 
  opts={}
) {
  if (!date) return null;
  const dt = new Date(date)
  const tzAgnostic = new Date(dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000);
  return formatDate(tzAgnostic, formatStr, opts);
}

export const formatTime = (timeStr: string) => {
  const [hours, minutes] = timeStr.split(':').map(Number);
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12; // Convert 0 to 12 for 12 AM
  return `${displayHours}:${minutes.toString().padStart(2, '0')} ${period}`;
};

export const formatSeconds = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
    .toString()
    .padStart(2, "0")}`;
};
