import type { Team, TeamMember } from '@root/types/team';
import {
  JsonApiData,
  JsonApiDocument, JsonResourceIdentifier,
  type JsonResourceIdentifierType,
  transformResourceArrayToObject,
  useHttpApi,
} from '@kwai/api';
import { z } from 'zod';
import { type Ref, ref, toValue } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import { CountryResourceSchema } from '@root/composables/useCountry';

const TeamMemberSchema = JsonApiData.extend({
  type: z.literal('team_members'),
  attributes: z.object({
    name: z.string(),
  }),
});

export interface Teams {
  meta: {
    count: number,
    offset: number,
    limit: number
  },
  items: Team[]
}

const TeamResourceSchema = JsonApiData.extend({
  type: z.literal('teams'),
  attributes: z.object({
    name: z.string(),
    active: z.boolean(),
    remark: z.string(),
  }),
  relationships: z.object({
    team_members: z.object({
      data: z.array(JsonResourceIdentifier).default([]),
    }),
  }),
});

type TeamResource = z.infer<typeof TeamResourceSchema>;

export const TeamDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    TeamResourceSchema,
    z.array(TeamResourceSchema),
  ]),
  included: z.array(z.union([TeamMemberSchema, CountryResourceSchema])).default([]),
});
export type TeamDocument = z.infer<typeof TeamDocumentSchema>;

export const transform = (doc: TeamDocument) : Team | Teams => {
  const included = transformResourceArrayToObject(doc.included);
  const mapModel = (teamResource: TeamResource): Team => {
    const teamMembers: TeamMember[] = [];
    for (const teamMemberIdentifier of teamResource.relationships.team_members.data) {
      const teamMember = included[teamMemberIdentifier.type][teamMemberIdentifier.id as string];
      const countryResourceId = teamMember.relationships!.nationality.data as JsonResourceIdentifierType;
      const nationality = included[countryResourceId.type][countryResourceId.id as string];
      teamMembers.push(
        {
          id: teamMemberIdentifier.id as string,
          name: teamMember.attributes.name,
          license: {
            number: teamMember.attributes.license_number,
            end_date: teamMember.attributes.license_end_date,
          },
          gender: teamMember.attributes.gender,
          birthdate: teamMember.attributes.birthdate,
          nationality: {
            iso2: nationality.attributes.iso_2,
            iso3: nationality.attributes.iso_3,
            name: nationality.attributes.name,
          },
        }
      );
    }

    return {
      id: teamResource.id,
      name: teamResource.attributes.name,
      active: teamResource.attributes.active,
      remark: teamResource.attributes.remark,
      members: teamMembers,
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

const getTeams = async({
  offset = null,
  limit = null,
} : {
  offset?: number | null,
  limit?: number | null,
}) => {
  let api = useHttpApi().url('/v1/teams');
  if (offset) {
    api = api.query({ 'page[offset]': offset });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit });
  }
  return api.get().json().then(json => {
    const result = TeamDocumentSchema.safeParse(json);
    if (result.success) {
      return transform(result.data) as Teams;
    }
    console.log(result.error);
    throw result.error;
  });
};

export const useTeams = ({ offset = ref(0), limit = ref(0) } : { offset?: Ref<number>, limit?: Ref<number>}) => {
  const queryKey : { offset: Ref<number>, limit: Ref<number> } = { offset, limit };
  return useQuery({
    queryKey: ['club/teams', queryKey],
    queryFn: () => getTeams({
      offset: toValue(offset),
      limit: toValue(limit),
    }),
  });
};
