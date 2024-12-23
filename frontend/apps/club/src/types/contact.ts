import type { Country } from './country';

export interface Contact {
  emails: string[],
  tel: string,
  mobile: string,
  address: string,
  postalCode: string,
  city: string,
  county: string,
  country: Country
}
