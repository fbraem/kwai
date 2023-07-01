import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';
import { JsonApiDocument, useHttp } from '@kwai/api';
import { z } from 'zod';
import useSWRV from 'swrv';

const JsonApiApplication = z.object({
  id: z.string(),
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
    short_description: z.string(),
    description: z.string(),
  }),
});
type JsonApiApplicationType = z.infer<typeof JsonApiApplication>;

const JsonApiApplicationData = z.object({
  data: z.union([JsonApiApplication, z.array(JsonApiApplication).default([])]),
});
const JsonApiApplicationDocument = JsonApiDocument.extend(JsonApiApplicationData.shape);
type JsonApiApplicationDocumentType = z.infer<typeof JsonApiApplicationDocument>;

interface Application {
  id: string,
  name: string,
  title: string,
  short_description: string,
  description: string
}

export const useApplicationStore = defineStore(
  'applications',
  () => {
    const applications = ref<Application[]>([]);

    const activeApplicationName = ref<string|null>(null);
    const setActiveApplication = (name: string) => {
      activeApplicationName.value = name;
    };
    const activeApplication = computed<Application|null>(() => {
      if (activeApplicationName.value !== null) {
        return applications.value.find(application => application.name === activeApplicationName.value) || null;
      }
      return null;
    });

    const toModel = (json: JsonApiApplicationDocumentType): Application | Application[] => {
      const mapModel = (d: JsonApiApplicationType): Application => {
        return {
          id: d.id,
          title: d.attributes.title,
          name: d.attributes.name,
          short_description: d.attributes.short_description,
          description: d.attributes.description,
        };
      };
      if (Array.isArray(json.data)) {
        return json.data.map(mapModel);
      }
      return mapModel(json.data);
    };

    const load = () => {
      const { data, isValidating, error } = useSWRV<JsonApiApplicationDocumentType>(
        'portal.applications',
        () => {
          const api = useHttp()
            .url('/v1/portal/applications');
          return api.get().json();
        },
        {
          revalidateOnFocus: false,
        }
      );

      watch(
        data,
        (nv) => {
          const result = JsonApiApplicationDocument.safeParse(nv);
          if (result.success) {
            applications.value = <Application[]> toModel(result.data);
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
      applications,
      setActiveApplication,
      activeApplication,
      load,
    };
  }
);
