import type { DateType } from '@kwai/date';
import type { Contact } from './contact';
import type { Country } from './country';

export interface Person {
  firstName: string,
  lastName: string,
  gender: number,
  birthdate: DateType,
  remark: string,
  contact: Contact,
  nationality: Country
}
