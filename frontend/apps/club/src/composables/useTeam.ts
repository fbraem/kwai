import type { Team, TeamMember } from '@root/types/team';
import {
  JsonApiData,
  JsonApiDocument,
  JsonResourceIdentifier,
  type JsonResourceIdentifierType,
  transformResourceArrayToObject,
  useHttpApi,
} from '@kwai/api';
import { z } from 'zod';
import { type Ref, ref, toValue } from 'vue';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import { CountryResourceSchema } from '@root/composables/useCountry';
import { TeamMemberResourceSchema } from '@root/composables/useTeamMember';

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
  included: z.array(z.union([TeamMemberResourceSchema, CountryResourceSchema])).default([]),
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
          active: teamMember.attributes.active,
          firstName: teamMember.attributes.first_name,
          lastName: teamMember.attributes.last_name,
          license: {
            number: teamMember.attributes.license_number,
            endDate: teamMember.attributes.license_end_date,
          },
          gender: teamMember.attributes.gender,
          birthdate: teamMember.attributes.birthdate,
          nationality: {
            id: nationality.id as string,
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

const getTeam = (id: string) : Promise<Team> => {
  return useHttpApi()
    .url(`/v1/teams/${id}`)
    .get()
    .json()
    .then(json => {
      const result = TeamDocumentSchema.safeParse(json);
      if (result.success) {
        return transform(result.data) as Team;
      }
      throw result.error;
    });
};

export const useTeam = (id: Ref<string>) => {
  return useQuery({
    queryKey: ['club/teams', id],
    queryFn: () => getTeam(toValue(id)),
  });
};

const mutateTeam = (team: Team): Promise<Team> => {
  const payload: TeamDocument = {
    data: {
      id: team.id,
      type: 'teams',
      attributes: {
        name: team.name,
        active: team.active,
        remark: team.remark,
      },
      relationships: {
        team_members: {
          data: [],
        },
      },
    },
    included: [],
  };
  if (team.id) { // Update
    return useHttpApi()
      .url(`/v1/teams/${team.id}`)
      .patch(payload)
      .json(json => {
        const result = TeamDocumentSchema.safeParse(json);
        if (result.success) {
          return transform(result.data) as Team;
        }
        throw result.error;
      })
    ;
  }
  // Create
  return useHttpApi()
    .url('/v1/teams')
    .post(payload)
    .json(json => {
      const result = TeamDocumentSchema.safeParse(json);
      if (result.success) {
        return transform(result.data) as Team;
      }
      throw result.error;
    });
};

type OnSuccessCallback = () => void;
type OnSuccessAsyncCallback = () => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

export const useTeamMutation = ({ onSuccess }: MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Team) => mutateTeam(data),
    onSuccess: async(data: Team) => {
      queryClient.setQueryData(['club/teams', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess();
        } else {
          onSuccess();
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['club/teams'],
      exact: true,
    }),
  });
};
