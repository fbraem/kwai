import type { TeamMember } from '@root/types/team';
import {
  JsonApiData,
  JsonApiDocument,
  JsonResourceIdentifier,
  type JsonResourceIdentifierType,
  type ResourceItems,
  transformResourceArrayToObject,
  useHttpApi,
} from '@kwai/api';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import { z } from 'zod';
import { CountryResourceSchema } from '@root/composables/useCountry';
import { type Ref, ref, toValue } from 'vue';
import { createDateFromString } from '@kwai/date';

export const TeamMemberResourceSchema = JsonApiData.extend({
  type: z.literal('team_members'),
  attributes: z.object({
    active: z.boolean(),
    first_name: z.string(),
    last_name: z.string(),
    license_number: z.string(),
    license_end_date: z.string(),
    gender: z.number(),
    birthdate: z.string(),
    active_in_club: z.boolean(),
  }),
  relationships: z.object({
    nationality: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type TeamMemberResource = z.infer<typeof TeamMemberResourceSchema>;

export const TeamMemberDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    TeamMemberResourceSchema,
    z.array(TeamMemberResourceSchema),
  ]),
  included: z.array(CountryResourceSchema).default([]),
});
export type TeamMemberDocument = z.infer<typeof TeamMemberDocumentSchema>;

type TeamMembers = ResourceItems<TeamMember>;

export const transform = (doc: TeamMemberDocument) : TeamMember | TeamMembers => {
  const included = transformResourceArrayToObject(doc.included);
  const mapModel = (teamMemberResource: TeamMemberResource): TeamMember => {
    const countryResourceId = teamMemberResource.relationships!.nationality.data as JsonResourceIdentifierType;
    const nationality = included[countryResourceId.type][countryResourceId.id as string];
    return {
      id: teamMemberResource.id as string,
      active: teamMemberResource.attributes.active,
      firstName: teamMemberResource.attributes.first_name,
      lastName: teamMemberResource.attributes.last_name,
      license: {
        number: teamMemberResource.attributes.license_number,
        endDate: createDateFromString(teamMemberResource.attributes.license_end_date),
      },
      gender: teamMemberResource.attributes.gender,
      birthdate: createDateFromString(teamMemberResource.attributes.birthdate),
      nationality: {
        id: nationality.id as string,
        iso2: nationality.attributes.iso_2,
        iso3: nationality.attributes.iso_3,
        name: nationality.attributes.name,
      },
      activeInClub: teamMemberResource.attributes.active_in_club,
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

export interface TeamFilter {
  id: string,
  inTeam: boolean,
}

const getTeamMembers = async({
  offset = null,
  limit = null,
  team = null,
} : {
  offset?: number | null,
  limit?: number | null,
  team?: TeamFilter | null,
}) => {
  let api = useHttpApi().url('/v1/teams/members');
  if (offset) {
    api = api.query({ 'page[offset]': offset });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit });
  }
  if (team) {
    if (team.inTeam) {
      api = api.query({ 'filter[team]': team.id });
    } else {
      api = api.query({ 'filter[team]': `noteq:${team.id}` });
    }
  }
  return api
    .get()
    .json()
    .then(json => {
      const result = TeamMemberDocumentSchema.safeParse(json);
      if (result.success) {
        return transform(result.data) as TeamMembers;
      }
      throw result.error;
    });
};

export const useTeamMembers = ({
  offset = ref(0),
  limit = ref(0),
  team = ref(null),
} : {
  offset?: Ref<number>,
  limit?: Ref<number>,
  team?: Ref<TeamFilter|null>,
}) => {
  const queryKey = ['club/team_members'];
  if (team.value) {
    queryKey.push(team.value.id);
  }
  return useQuery({
    queryKey,
    queryFn: () => getTeamMembers({
      offset: toValue(offset),
      limit: toValue(limit),
      team: toValue(team),
    }),
  });
};

export interface TeamMemberData {
  team_id: string,
  member: TeamMemberDocument,
}

const mutateAddTeamMember = (data: TeamMemberData): Promise<TeamMember> => {
  const payload = data.member;
  return useHttpApi()
    .url(`/v1/teams/${data.team_id}/members`)
    .post(payload)
    .json(json => {
      const result = TeamMemberDocumentSchema.safeParse(json);
      if (result.success) {
        return transform(result.data) as TeamMember;
      }
      throw result.error;
    });
};

interface MutationOptions {
  onSuccess?: (data: TeamMember, variables: TeamMemberData) => Promise<void> | void
}

export const useAddTeamMemberMutation = ({ onSuccess }: MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (variables: TeamMemberData) => mutateAddTeamMember(variables),
    onSuccess: (data: TeamMember, variables: TeamMemberData) => {
      if (onSuccess) {
        return onSuccess(data, variables);
      }
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({
        queryKey: ['club/teams', variables.team_id],
        exact: true,
      });
    },
  });
};

/**
 * Returns a function that can be used to remove the team member
 * from the club/team_members/<team_id> cache.
 */
export const useUpdateTeamMemberCache = () => {
  const queryClient = useQueryClient();

  return (teamMember: TeamMember, variables: TeamMemberData) => {
    queryClient.setQueryData(
      ['club/team_members', variables.team_id],
      (oldData: ResourceItems<TeamMember>) => {
        return {
          ...oldData,
          items: oldData.items.filter(item => item.id !== teamMember.id),
        };
      }
    );
  };
};
