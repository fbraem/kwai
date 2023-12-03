import { describe, expect, it } from 'vitest';
import { createDateFromString } from '../src';

describe('getter', () => {
  it('can get the day of the month', () => {
    const date = createDateFromString('1860-10-28');
    expect(date.dayOfMonth()).eq(28);
  });
  it('can get the day of the week', () => {
    const date = createDateFromString('1860-10-28');
    expect(date.dayOfWeek()).eq(0);
  });
});
