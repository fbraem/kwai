/* Defines JSON:API schemas with valibot */

import * as v from 'valibot';

export const JsonApiIdentifierSchema = v.object({
  id: v.optional(v.string()),
  type: v.string(),
});

export const createIdentifierSchema = (type: string) => {
  return v.object({
    ...JsonApiIdentifierSchema.entries,
    type: v.literal(type),
  });
};

export const JsonApiRelationshipSchema = v.object({ data: v.union([JsonApiIdentifierSchema, v.array(JsonApiIdentifierSchema)]) });

export const JsonApiDataSchema = v.object({
  ...JsonApiIdentifierSchema.entries,
  meta: v.optional(v.record(v.string(), v.any())),
  attributes: v.record(v.string(), v.any()),
  relationships: v.optional(v.record(v.string(), JsonApiRelationshipSchema)),
});

export const JsonApiErrorSchema = v.object({
  status: v.optional(v.string(), ''),
  source: v.optional(v.object({ pointer: v.string() })),
  title: v.optional(v.string(), ''),
  detail: v.optional(v.string(), ''),
});

export const JsonApiDocumentSchema = v.object({
  meta: v.optional(
    v.object({
      count: v.optional(v.number(), 0),
      limit: v.optional(v.number(), 0),
      offset: v.optional(v.number(), 0),
    })
  ),
  data: v.union([JsonApiDataSchema, v.array(JsonApiDataSchema)]),
  included: v.optional(v.array(JsonApiDataSchema), []),
  errors: v.optional(v.array(JsonApiErrorSchema)),
});
