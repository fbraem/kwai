import dayjs, { ManipulateType, OpUnitType } from 'dayjs';

// Load all necessary extensions
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';
import localizedFormat from 'dayjs/plugin/localizedFormat.js';
import localeData from 'dayjs/plugin/localeData.js';
import weekday from 'dayjs/plugin/weekday.js';
import customParseFormat from 'dayjs/plugin/customParseFormat.js';

// Set the locale
import 'dayjs/locale/en.js';
import 'dayjs/locale/nl.js';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(localizedFormat);
dayjs.extend(localeData);
dayjs.extend(weekday);
dayjs.extend(customParseFormat);
// TODO: For now, use the nl locale, in the future this must be configurable.
dayjs.locale('nl');

export interface DateType {
  add(n: number, unit: string): DateType;
  day(): number;
  endOf(unit: string): DateType;
  format(format?: string): string;
  month(): number;
  startOf(unit: string): DateType;
  toDate(): Date;
  utc(): DateType;
  year(): number;
}

function wrapDayjs(d: dayjs.Dayjs): DateType {
  const value = d;

  function add(n: number, unit: string): DateType {
    return wrapDayjs(d.add(n, <ManipulateType> unit));
  }

  function day(): number {
    return d.day();
  }

  function endOf(unit: string): DateType {
    return wrapDayjs(d.endOf(<OpUnitType> unit));
  }

  function format(format: string = 'YYYY-MM-DD'): string {
    return d.format(format);
  }

  function month(): number {
    return d.month();
  }

  function startOf(unit: string): DateType {
    return wrapDayjs(d.startOf(<OpUnitType> unit));
  }

  function toDate(): Date {
    return d.toDate();
  }

  function utc(): DateType {
    return wrapDayjs(d.utc());
  }

  function year(): number {
    return d.year();
  }

  return Object.freeze({
    value,
    add,
    day,
    endOf,
    format,
    month,
    startOf,
    toDate,
    utc,
    year,
  });
}

export function createFromDate(d: Date): DateType {
  return wrapDayjs(dayjs(d));
}

export function createDate(year?: number | null, month?: number | null, day?: number | null): DateType {
  year = year || dayjs().year();
  month = month || dayjs().month();
  day = day || dayjs().date();
  return createFromDate(new Date(year, month, day));
}

export function createDateFromString(value?: string, fmt: string = 'YYYY-MM-DD'): DateType {
  return wrapDayjs(value ? dayjs(value, fmt) : dayjs());
}

export function createDatetimeFromString(value?: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): DateType {
  return createDateFromString(value, fmt);
}

export function createDateTimeFromUTC(value: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): DateType {
  return wrapDayjs(dayjs.utc(value, fmt).tz());
}

export function now(): DateType {
  return createDateFromString();
}

export function getLocaleFormat(format: string = 'L'): string {
  return dayjs.localeData().longDateFormat(format);
}
