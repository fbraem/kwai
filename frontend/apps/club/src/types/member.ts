import type { DateType } from '@kwai/date';
import type { Person } from './person';

interface License {
  number: string,
  end_date: DateType
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
