import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';

dayjs.extend(utc)
dayjs.extend(timezone)

export const serverFormat = 'YYYY-MM-DD HH:mm:ss';

export function zonedToUtc(datetime, tz, format = serverFormat) {
  return dayjs.tz(datetime, tz).tz('utc').utc().format(format)
}

export function utcToZoned(datetime, tz, format = serverFormat) {
  return dayjs.utc(datetime).tz(tz).format(format);
}

export function formatDatetime(datetime, format = serverFormat) {
  return dayjs(datetime).format(format);
}

export function userTimezone() {
  return dayjs.tz.guess();
}

export function diffInDays(startDate, endDate) {
  let start = dayjs(startDate);
  let end = dayjs(endDate);

  return end.diff(start, 'day');
}
