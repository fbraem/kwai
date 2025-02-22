import Cookies from 'universal-cookie';
import wretch from 'wretch';
import FormDataAddon from 'wretch/addons/formData';
import QueryStringAddon from 'wretch/addons/queryString';
import * as z from 'zod';

export * from './jsonapi';

export const JsonResourceIdentifier = z.object({
  id: z.optional(z.string()),
  type: z.string(),
});
export type JsonResourceIdentifierType = z.infer<typeof JsonResourceIdentifier>;

export const JsonApiRelationship = z.object({ data: z.union([JsonResourceIdentifier, z.array(JsonResourceIdentifier)]) });

export const JsonApiData = JsonResourceIdentifier.extend({
  attributes: z.record(z.string(), z.any()),
  meta: z.record(z.string(), z.any()).optional(),
  relationships: z.record(z.string(), JsonApiRelationship).optional(),
});
export type JsonApiDataType = z.infer<typeof JsonApiData>;

export const JsonApiError = z.object({
  status: z.string().default(''),
  source: z.object({ pointer: z.string() }).optional(),
  title: z.string().default(''),
  detail: z.string().default(''),
});
export type JsonApiErrorType = z.infer<typeof JsonApiError>;

export const JsonApiDocument = z.object({
  meta: z
    .object({
      count: z.number().optional(),
      limit: z.optional(z.nullable(z.number())),
      offset: z.optional(z.nullable(z.number())),
    })
    .optional(),
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
export const transformResourceArrayToObject = (
  resources: JsonApiDataType[]
): Record<string, Record<string, JsonApiDataType>> => {
  return resources.reduce(
    (acc: Record<string, Record<string, JsonApiDataType>>, current) => {
      if (!acc[current.type]) {
        acc[current.type] = {};
      }
      acc[current.type][current.id as string] = current;
      return acc;
    },
    {}
  );
};

/**
 * An interface that can be used for the result of a transform of a document
 * with multiple resources.
 */
export interface ResourceItems<T> {
  meta: {
    count: number
    offset: number
    limit: number
  }
  items: T[]
}

export const isLoggedIn = (): boolean => {
  const cookies = new Cookies(null, { path: '/' });
  return cookies.get('kwai') !== undefined;
};

export const useHttp = () =>
  wretch('/api', {
    credentials: 'include',
    mode: 'cors',
  })
    .addon(FormDataAddon)
    .addon(QueryStringAddon);

const renewToken = async() => {
  await useHttp()
    .url('/v1/auth/access_token')
    .post()
    .json()
    .catch((error) => {
      console.log(error);
    });
};
let activeRenewTokenRequest: Promise<void> | null = null;

export const useHttpWithAuthCatcher = () =>
  useHttp().catcher(401, async(err, request) => {
    if (activeRenewTokenRequest == null) {
      activeRenewTokenRequest = renewToken();
    }
    await activeRenewTokenRequest;
    activeRenewTokenRequest = null;

    return request
      .fetch()
      .unauthorized((err) => {
        throw err;
      })
      .json();
  });

interface LoginFormData {
  username: string
  password: string
}

export const useHttpLogin = (loginFormData: LoginFormData) => {
  return useHttp().formData(loginFormData).url('/v1/auth/login').post().res();
};

export const useHttpApi = () =>
  useHttpWithAuthCatcher().accept('application/vnd.api+json');
//  .content('application/vnd.api+json')

export interface Pagination {
  offset?: number
  limit?: number
}

export const useHttpPaginationApi = ({ offset = 0, limit = 0 }: Pagination) => {
  return useHttpApi()
    .query({
      'page[offset]': offset,
      'page[limit]': limit,
    });
};

export const useHttpLogout = async() => {
  await useHttp()
    .url('/v1/auth/logout')
    .post()
    .res()
    .catch((error) => {
      if (error.response) {
        // Ignore 401, tokens are already revoked
        if (error.response.status !== 401) {
          throw error;
        }
      }
    });
};
