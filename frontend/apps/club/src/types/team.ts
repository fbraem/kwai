import type { License } from '@root/types/member';
import type { Country } from '@root/types/country';
import type { DateType } from '@kwai/date';

export interface TeamMember {
  id: string,
  active: boolean,
  firstName: string,
  lastName: string,
  license: License,
  gender: number,
  birthdate: DateType,
  nationality: Country,
  activeInClub: boolean
}

export interface Team {
  id?: string,
  name: string,
  active: boolean,
  remark: string,
  members: TeamMember[],
}
