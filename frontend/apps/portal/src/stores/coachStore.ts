import { defineStore } from 'pinia';
import type { Ref } from 'vue';
import { ref, watch } from 'vue';
import useSWRV from 'swrv';
import { z } from 'zod';
import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';

const JsonApiMember = z.object({
  id: z.string(),
  type: z.literal('members'),
  attributes: z.object({
    name: z.string(),
  }),
});
type JsonApiMemberType = z.infer<typeof JsonApiMember>;

const JsonApiCoach = z.object({
  id: z.string(),
  type: z.literal('coaches'),
  attributes: z.object({
    bio: z.nullable(z.string()),
    diploma: z.nullable(z.string()),
  }),
  relationships: z.object({
    member: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type JsonApiCoachType = z.infer<typeof JsonApiCoach>;

const JsonApiCoachData = z.object({
  data: z.union([JsonApiCoach, z.array(JsonApiCoach).default([])]),
  included: z.array(JsonApiMember).default([]),
});

const JsonApiCoachDocument = JsonApiDocument.extend(JsonApiCoachData.shape);
type JsonApiCoachDocumentType = z.infer<typeof JsonApiCoachDocument>;

export type Coach = {
  id: string,
  name: string,
  bio: string|null,
  diploma: string|null
}

const toModel = (json: JsonApiCoachDocumentType): Coach | Coach[] => {
  const mapModel = (d: JsonApiCoachType): Coach => {
    const member = <JsonApiMemberType> json.included.find(
      included => included.type === JsonApiMember.shape.type.value && included.id === d.relationships.member.data.id
    );
    return {
      id: d.id,
      name: member?.attributes.name ?? 'Unknown Coach',
      bio: d.attributes.bio,
      diploma: d.attributes.diploma,
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

export const useCoachStore = defineStore('portal.coaches', () => {
  const coaches: Ref<Coach[]> = ref([]);

  const load = () => {
    const { data, isValidating, error } = useSWRV<JsonApiCoachDocumentType>(
      'portal.coaches',
      () => {
        const api = useHttpApi().url('/coaches');
        return api
          .get()
          .json()
        ;
      },
      {
        revalidateOnFocus: false,
      }
    );

    watch(
      data,
      (nv) => {
        const result = JsonApiCoachDocument.safeParse(nv);
        if (result.success) {
          coaches.value = <Coach[]> toModel(result.data);
        } else {
          console.log(result.error);
        }
      }
    );

    return {
      loading: isValidating,
      error,
    };
  };

  return {
    coaches,
    load,
  };
});
