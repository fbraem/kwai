import { describe, expect, it } from 'vitest';
import { createDateFromString } from '../src';

describe('manipulate', () => {
  it('can add a day', () => {
    const dateNow = new Date();
    const dateTomorrow = new Date();
    dateTomorrow.setDate(dateNow.getDate() + 1);

    const now = createDateFromString();
    const tomorrow = now.add(1, 'd');
    expect(tomorrow.day()).eq(dateTomorrow.getDay());
  });

  it('can copy units', () => {
    const date1 = createDateFromString('2023-12-01');
    const date2 = createDateFromString('2024-01-01');

    const newDate = date1.copy(date2, ['year', 'month']);
    console.log(newDate.format('YYYY-MM-DD'));
    expect(newDate.get('year')).eq(2024);
    expect(newDate.get('month')).eq(0);
  });
});
