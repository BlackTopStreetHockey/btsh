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