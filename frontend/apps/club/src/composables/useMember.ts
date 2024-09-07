import { createDateFromString } from '@kwai/date';
import { JsonApiData, JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { type Ref, ref, toValue } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import { z } from 'zod';
import type { Member } from '@root/types/member';
import { CountryResourceSchema } from '@root/composables/useCountry';

export interface Members {
  meta: { count: number, offset: number, limit: number },
  items: Member[]
}

const MemberResourceSchema = JsonApiData.extend({
  type: z.literal('members'),
  attributes: z.object({
    license_number: z.string(),
    license_end_date: z.string(),
    active: z.boolean(),
    competition: z.boolean(),
    remark: z.string(),
  }),
  relationships: z.object({
    person: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type MemberResource = z.infer<typeof MemberResourceSchema>;

const PersonResourceSchema = JsonApiData.extend({
  type: z.literal('persons'),
  attributes: z.object({
    first_name: z.string(),
    last_name: z.string(),
    gender: z.number(),
    birthdate: z.string(),
    remark: z.string(),
  }),
  relationships: z.object({
    contact: z.object({
      data: JsonResourceIdentifier,
    }),
    nationality: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type PersonResource = z.infer<typeof PersonResourceSchema>;

const ContactResourceSchema = JsonApiData.extend({
  type: z.literal('contacts'),
  attributes: z.object({
    emails: z.array(z.string()),
    tel: z.string(),
    mobile: z.string(),
    address: z.string(),
    postal_code: z.string(),
    city: z.string(),
    county: z.string(),
    remark: z.string(),
  }),
  relationships: z.object({
    country: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type ContactResource = z.infer<typeof ContactResourceSchema>;

export const MemberDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    MemberResourceSchema,
    z.array(MemberResourceSchema).default([]),
  ]),
  included: z.array(
    z.union([
      PersonResourceSchema,
      ContactResourceSchema,
      CountryResourceSchema,
    ])
  ).default([]),
});
type MemberDocument = z.infer<typeof MemberDocumentSchema>;

export const transform = (doc: MemberDocument) : Member | Members => {
  const mapModel = (data: MemberResource): Member => {
    const person = doc.included.find(included => included.type === PersonResourceSchema.shape.type.value && included.id === data.relationships.person.data.id) as PersonResource;
    const nationality = doc.included.find(included => included.type === CountryResourceSchema.shape.type.value && included.id === person.relationships.nationality.data.id) as CountryResource;
    const contact = doc.included.find(included => included.type === ContactResourceSchema.shape.type.value && included.id === person.relationships.contact.data.id) as ContactResource;
    const country = doc.included.find(included => included.type === CountryResourceSchema.shape.type.value && included.id === contact.relationships.country.data.id) as CountryResource;

    return {
      id: data.id,
      new: data.meta?.new ?? false,
      active: data.attributes.active,
      competition: data.attributes.competition,
      remark: data.attributes.remark,
      license: {
        number: data.attributes.license_number,
        end_date: createDateFromString(data.attributes.license_end_date),
      },
      person: {
        birthdate: createDateFromString(person.attributes.birthdate),
        contact: {
          address: contact.attributes.address,
          city: contact.attributes.city,
          country: {
            name: country.attributes.name,
            iso2: country.attributes.iso_2,
            iso3: country.attributes.iso_3,
          },
          county: contact.attributes.county,
          emails: contact.attributes.emails,
          mobile: contact.attributes.mobile,
          tel: contact.attributes.tel,
          postalCode: contact.attributes.postal_code,
        },
        remark: person.attributes.remark,
        firstName: person.attributes.first_name,
        lastName: person.attributes.last_name,
        gender: person.attributes.gender,
        nationality: {
          name: nationality.attributes.name,
          iso2: nationality.attributes.iso_2,
          iso3: nationality.attributes.iso_3,
        },
      },
    };
  };
  if (Array.isArray(doc.data)) {
    return {
      meta: {
        count: doc.meta?.count || 0,
        offset: doc.meta?.offset || 0,
        limit: doc.meta?.limit || 0,
      },
      items: doc.data.map(mapModel),
    };
  }
  return mapModel(doc.data);
};

const getMembers = async({
  offset = null,
  limit = null,
} : {
  offset?: number | null,
  limit?: number | null
}) : Promise<Members> => {
  let api = useHttpApi()
    .url('/v1/club/members')
  ;
  if (offset) {
    api = api.query({ 'page[offset]': offset });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit });
  }
  return api.get().json().then(json => {
    const result = MemberDocumentSchema.safeParse(json);
    if (result.success) {
      return transform(result.data) as Members;
    }
    console.log(result.error);
    throw result.error;
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
