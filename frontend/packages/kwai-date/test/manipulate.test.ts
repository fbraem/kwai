import { describe, expect, it } from 'vitest';
import { createDate } from '@kwai/date';

describe('manipulate', () => {
  it('can add a day', () => {
    const dateNow = new Date();
    const dateTomorrow = new Date();
    dateTomorrow.setDate(dateNow.getDate() + 1);

    const now = createDate();
    const tomorrow = now.add(1, 'd');
    expect(tomorrow.day()).eq(dateTomorrow.getDay());
  });
});
