import type { DateType } from '@kwai/date';
import { useHttpApi } from '@kwai/api';
import { type Ref, ref, toValue } from 'vue';
import { useQuery } from '@tanstack/vue-query';

interface Country {
  iso2: string,
  iso3: string,
  name: string
}
interface Contact {
  emails: string[],
  tel: string,
  mobile: string,
  address: string,
  postalCode: string,
  city: string,
  county: string,
  country: Country
}

interface Person {
  firstName: string,
  lastName: string,
  gender: number,
  birthdate: DateType,
  remark: string,
  contact: Contact,
  nationality: Country
}

interface License {
  number: string,
  end_date: DateType
}

interface Member {
  license: License,
  remark: string,
  active: boolean,
  competition: boolean
  person: Person
}

const getMembers = async({
  offset = null,
  limit = null,
} : {
  offset?: number | null,
  limit?: number | null
}) => {
  const api = useHttpApi()
    .url('/v1/club/members')
  ;
  return api.get().json().then(json => {
    console.log(json);
    return json;
  });
};

export const useMembers = ({ offset = ref(0), limit = ref(0) } : { offset?: Ref<number>, limit?: Ref<number>}) => {
  const queryKey : { offset: Ref<number>, limit: Ref<number> } = { offset, limit };
  return useQuery({
    queryKey: ['club/members', queryKey],
    queryFn: () => getMembers({
      offset: toValue(offset),
      limit: toValue(limit),
    }),
  });
};
