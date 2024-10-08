import dayjs, { ManipulateType, OpUnitType, UnitType } from 'dayjs';

// Load all necessary extensions
import utcPlugin from 'dayjs/plugin/utc.js';
import timezonePlugin from 'dayjs/plugin/timezone.js';
import localizedFormatPlugin from 'dayjs/plugin/localizedFormat.js';
import localeDataPlugin from 'dayjs/plugin/localeData.js';
import weekdayPlugin from 'dayjs/plugin/weekday.js';
import customParseFormatPlugin from 'dayjs/plugin/customParseFormat.js';

// Set the locale
import 'dayjs/locale/en.js';
import 'dayjs/locale/nl.js';

dayjs.extend(utcPlugin);
dayjs.extend(timezonePlugin);
dayjs.extend(localizedFormatPlugin);
dayjs.extend(localeDataPlugin);
dayjs.extend(weekdayPlugin);
dayjs.extend(customParseFormatPlugin);
// TODO: For now, use the nl locale, in the future this must be configurable.
dayjs.locale('nl');

export interface DateType {
  add(n: number, unit: string): DateType;
  copy(from: DateType, unit: string | string[]): DateType;
  dayOfWeek(): number;
  dayOfMonth(): number;
  endOf(unit: string): DateType;
  format(format?: string): string;
  get(unit: string): number;
  isBefore(check: DateType): boolean;
  month(): number;
  set(unit: string, value: number): DateType;
  startOf(unit: string): DateType;
  toDate(): Date;
  utc(): DateType;
  value: dayjs.Dayjs;
  year(): number;
}

function wrapDayjs(d: dayjs.Dayjs): DateType {
  const value = d;

  function add(n: number, unit: string): DateType {
    return wrapDayjs(value.add(n, <ManipulateType> unit));
  }

  function copy(from: DateType, unit: string | string[]): DateType {
    if (typeof unit === 'string') {
      unit = [unit];
    }
    let newValue = value;
    for (const u of unit) {
      newValue = newValue.set(u as UnitType, from.get(u as UnitType));
    }
    return wrapDayjs(newValue);
  }

  function dayOfMonth(): number {
    return value.date();
  }

  function dayOfWeek(): number {
    return value.day();
  }

  function endOf(unit: string): DateType {
    return wrapDayjs(value.endOf(<OpUnitType> unit));
  }

  function format(format: string = 'YYYY-MM-DD'): string {
    return value.format(format);
  }

  function get(unit: string): number {
    return value.get(<UnitType> unit);
  }

  function isBefore(check: DateType): boolean {
    return value.isBefore(check.value);
  }

  function month(): number {
    return value.month();
  }

  function set(unit: string, newValue: number): DateType {
    return wrapDayjs(value.set(<UnitType> unit, newValue));
  }

  function startOf(unit: string): DateType {
    return wrapDayjs(value.startOf(<OpUnitType> unit));
  }

  function toDate(): Date {
    return value.toDate();
  }

  function utc(): DateType {
    return wrapDayjs(value.utc());
  }

  function year(): number {
    return value.year();
  }

  return Object.freeze({
    add,
    copy,
    dayOfWeek,
    dayOfMonth,
    endOf,
    format,
    get,
    isBefore,
    month,
    set,
    startOf,
    toDate,
    utc,
    value,
    year,
  });
}

export function createFromDate(d: Date): DateType {
  return wrapDayjs(dayjs(d));
}

export function createDate(year?: number | null, month?: number | null, day?: number | null): DateType {
  year = year ?? dayjs().year();
  month = month ?? dayjs().month();
  day = day ?? dayjs().date();
  return createFromDate(new Date(year, month, day));
}

export function createDateFromString(value?: string, fmt: string = 'YYYY-MM-DD'): DateType {
  return wrapDayjs(value ? dayjs(value, fmt) : dayjs());
}

export function createDatetimeFromString(value?: string, timezone?: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): DateType {
  if (timezone) {
    return wrapDayjs(dayjs.tz(value, fmt, timezone).tz());
  }
  return wrapDayjs(value ? dayjs(value, fmt) : dayjs());
}

export function createDateTimeFromUTC(value: string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): DateType {
  return wrapDayjs(dayjs.utc(value, fmt).tz());
}

export function formatToUTC(value: DateType | null, fmt: string = 'YYYY-MM-DD HH:mm:ss'): string | null {
  return value?.utc().format(fmt) ?? null;
}

export function now(): DateType {
  return wrapDayjs(dayjs());
}

export function getLocaleFormat(format: string = 'L'): string {
  return dayjs.localeData().longDateFormat(format);
}

export function weekdays(): string[] {
  return dayjs.weekdays() as string[];
}

export function weekday(day: number): string {
  return weekdays()[day];
}
