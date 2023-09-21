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
  add(n: number, unit: string): Readonly<DateType>;
  day(): number;
  endOf(unit: string): Readonly<DateType>;
  format(format?: string): string;
  startOf(unit: string): Readonly<DateType>;
}

function wrapDayjs(d: dayjs.Dayjs): Readonly<DateType> {
  function add(n: number, unit: string): Readonly<DateType> {
    return wrapDayjs(d.add(n, <ManipulateType> unit));
  }

  function day(): number {
    return d.day();
  }

  function endOf(unit: string): Readonly<DateType> {
    return wrapDayjs(d.endOf(<OpUnitType> unit));
  }

  function format(format: string = 'YYYY-MM-DD'): string {
    return d.format(format);
  }

  function startOf(unit: string): Readonly<DateType> {
    return wrapDayjs(d.startOf(<OpUnitType> unit));
  }

  return Object.freeze({
    add,
    day,
    endOf,
    format,
    startOf,
  });
}

export function createDate(value?: string, fmt: string = 'YYYY-MM-DD'): Readonly<DateType> {
  return wrapDayjs(value ? dayjs(value, fmt) : dayjs());
}

export function createDatetime(value?: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): Readonly<DateType> {
  return createDate(value, fmt);
}

export function createDateTimeFromUTC(value: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): Readonly<DateType> {
  return wrapDayjs(dayjs.utc(value, fmt).tz());
}

export function now(): Readonly<DateType> {
  return createDate();
}
