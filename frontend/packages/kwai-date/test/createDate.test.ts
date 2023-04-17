import { describe, expect, it } from 'vitest';
import { createDate } from '@kwai/date';

describe('createDate', () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const stringMonth = month.toString().padStart(2, '0');
  const day = now.getDate();
  const stringDay = day.toString().padStart(2, '0');

  it('can create a date', () => {
    expect(createDate().format('YYYY-MM-DD')).eq(`${year}-${stringMonth}-${stringDay}`);
  });
  it('can format a date', () => {
    expect(createDate().format('DD-MM-YYYY')).eq(`${stringDay}-${stringMonth}-${year}`);
  });
});
