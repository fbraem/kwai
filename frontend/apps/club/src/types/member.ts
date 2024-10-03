import type { DateType } from '@kwai/date';
import type { Person } from './person';

export interface License {
  number: string,
  endDate: DateType
}

export interface Member {
  id?: string,
  license: License,
  remark: string,
  active: boolean,
  competition: boolean,
  person: Person,
  new: boolean
}
