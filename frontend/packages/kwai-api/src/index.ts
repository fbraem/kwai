import wretch from 'wretch';
import type { Ref } from 'vue';
import { computed } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import FormDataAddon from 'wretch/addons/formData';
import QueryStringAddon from 'wretch/addons/queryString';
import * as z from 'zod';

export const JsonResourceIdentifier = z.object({
  id: z.optional(z.string()),
  type: z.string(),
});
export type JsonResourceIdentifierType = z.infer<typeof JsonResourceIdentifier>;

export const JsonApiRelationship = z.object({
  data: z.union([JsonResourceIdentifier, z.array(JsonResourceIdentifier)]),
});

export const JsonApiData = JsonResourceIdentifier.extend({
  attributes: z.record(
    z.string(),
    z.any()
  ),
  meta: z.record(z.string(), z.any()).optional(),
  relationships: z.record(
    z.string(),
    JsonApiRelationship
  ).optional(),
});
export type JsonApiDataType = z.infer<typeof JsonApiData>;

export const JsonApiError = z.object({
  status: z.string().default(''),
  source: z.object({
    pointer: z.string(),
  }).optional(),
  title: z.string().default(''),
  detail: z.string().default(''),
});
export type JsonApiErrorType = z.infer<typeof JsonApiError>;

export const JsonApiDocument = z.object({
  meta: z.object({
    count: z.number().optional(),
    limit: z.optional(z.nullable(z.number())),
    offset: z.optional(z.nullable(z.number())),
  }).optional(),
  data: z.union([JsonApiData, z.array(JsonApiData)]),
  included: z.array(JsonApiData).optional(),
  errors: z.array(JsonApiError).optional(),
});
export type JsonApiDocumentType = z.infer<typeof JsonApiDocument>;

/**
 * Transforms an array of resources in a nested object.
 *
 * This object makes it easier to lookup included resources. When, for example, a team resource
 * has team members, the included array will contain resources for the team members but also
 * country resources for the nationality of these team members. In this example, the returned
 * object will have two properties: team_members and countries. The value of these properties will
 * be another object with all the resources. The property for each resource will be the id of the resource.
 *
 * {
 *   team_members: {
 *     '1': {
 *       type: 'team_members',
 *       id: '1',
 *       attributes: {
 *        name: 'Jigoro Kano',
 *       },
 *       relationships: {
 *         nationality: {
 *           data: { type: 'countries', 'id': '1' }
 *         }
 *       }
 *     }
 *   },
 *   countries: {
 *     '1': {
 *       type: 'countries',
 *       id: '1',
 *       attributes: {
 *         name: 'Japan'
 *       }
 *     }
 *   }
 * }
 *
 * @param resources
 */
export const transformResourceArrayToObject = (resources: JsonApiDataType[]): Record<string, Record<string, JsonApiDataType>> => {
  return resources.reduce((acc: Record<string, Record<string, JsonApiDataType>>, current) => {
    if (!acc[current.type]) {
      acc[current.type] = {};
    }
    acc[current.type][current.id as string] = current;
    return acc;
  }, {});
};

/**
 * An interface that can be used for the result of a transform of a document
 * with multiple resources.
 */
export interface ResourceItems<T> {
    meta: {
    count: number,
    offset: number,
    limit: number
  },
  items: T[]
}

export interface LocalStorage {
    loginRedirect: Ref<string|null>,
    accessToken: Ref<string|null>,
    refreshToken: Ref<string|null>
}
export const localStorage: LocalStorage = {
  loginRedirect: useLocalStorage('login_redirect', null),
  accessToken: useLocalStorage('access_token', null),
  refreshToken: useLocalStorage('refresh_token', null),
};

export const isLoggedIn = computed((): boolean => localStorage.accessToken.value != null);

interface Options {
    baseUrl?: string,
    accessToken?: Ref<string|null>,
    refreshToken?: Ref<string|null>
}

export const useHttp = (options: Options = {}) => wretch(
  '/api',
  {
    credentials: 'include',
    mode: 'cors',
  }
).addon(FormDataAddon).addon(QueryStringAddon);

interface AccessTokenJSON {
  access_token: string,
  refresh_token: string
}

export const useHttpAuth = (options: Options = {}) => useHttp(options).defer(
  w => {
    const accessToken = options.accessToken ?? localStorage.accessToken;
    if (accessToken.value) {
      return w.auth(`Bearer ${accessToken.value}`);
    }
    return w;
  })
;

const renewToken = async(options: Options = {}) => {
  const accessToken = localStorage.accessToken;
  const refreshToken = localStorage.refreshToken;

  const form = {
    refresh_token: refreshToken.value,
  };

  await useHttp(options)
    .url('/v1/auth/access_token')
    .formData(form)
    .post()
    .json()
    .then(json => {
      const token = <AccessTokenJSON> json;
      accessToken.value = token.access_token;
      refreshToken.value = token.refresh_token;
    })
    .catch(error => {
      accessToken.value = null;
      refreshToken.value = null;
      console.log(error);
    })
  ;
};
let activeRenewTokenRequest: Promise<void>|null = null;

export const useHttpWithAuthCatcher = (options: Options = {}) => useHttpAuth(options)
  .catcher(401, async(err, request) => {
    if (activeRenewTokenRequest == null) {
      activeRenewTokenRequest = renewToken(options);
    }
    await activeRenewTokenRequest;
    activeRenewTokenRequest = null;

    const accessToken = localStorage.accessToken;

    return request
      .auth(accessToken.value as string)
      .fetch()
      .unauthorized(err => { throw err; })
      .json()
    ;
  })
;

interface LoginFormData {
    username: string,
    password: string
}

export const useHttpLogin = (formData: LoginFormData, options: Options = {}) => {
  const accessToken = options.accessToken ?? localStorage.accessToken;
  accessToken.value = null;
  const refreshToken = options.refreshToken ?? localStorage.refreshToken;
  refreshToken.value = null;

  return useHttp(options)
    .url('/v1/auth/login')
    .formData(formData)
    .post()
    .json<AccessTokenJSON>()
    .then(json => {
      accessToken.value = json.access_token;
      refreshToken.value = json.refresh_token;
    });
};

export const useHttpForm = (formData: FormData, options: Options = {}) => {
  return useHttpAuth(options)
    .formData(formData)
  ;
};

export const useHttpApi = (options: Options = {}) => useHttpWithAuthCatcher(options)
  .accept('application/vnd.api+json')
//  .content('application/vnd.api+json')
;

export const useHttpLogout = async(options: Options = {}) => {
  const accessToken = options.accessToken ?? localStorage.accessToken;
  const refreshToken = options.refreshToken ?? localStorage.refreshToken;

  const form = {
    refresh_token: refreshToken.value,
  };

  await useHttpAuth(options)
    .url('/v1/auth/logout')
    .formData(form)
    .post()
    .res()
    .catch(error => {
      if (error.response) {
        // Ignore 401, tokens are already revoked
        if (error.response.status !== 401) {
          throw error;
        }
      }
    });

  accessToken.value = null;
  refreshToken.value = null;
};
