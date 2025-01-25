import {
  describe, expect, it,
} from 'vitest';
import * as v from 'valibot';

import { JsonApiDocumentSchema } from './jsonapi';

describe('it can perform type checking for JSONAPI', () => {
  it('can typecheck a simple structure', () => {
    const json = {
      data: {
        id: '1',
        type: 'members',
        attributes: {
          name: 'Jigoro Kano',
          year_of_birth: 1860,
        },
      },
    };

    const result = v.safeParse(JsonApiDocumentSchema, json);
    expect(result.success).toBeTruthy();
  });
  it('can typecheck a structure with a relationship', () => {
    const json = {
      data: {
        id: '1',
        type: 'members',
        attributes: {
          name: 'Jigoro Kano',
          year_of_birth: 1860,
        },
        relationships: {
          teams: {
            data: {
              id: '1',
              type: 'teams',
            },
          },
        },
      },
    };
    const result = v.safeParse(JsonApiDocumentSchema, json);
    expect(result.success).toBeTruthy();
  });

  it('can typecheck a structure with an array relationship', () => {
    const json = {
      data: {
        id: '1',
        type: 'members',
        attributes: {
          name: 'Jigoro Kano',
          year_of_birth: 1860,
        },
        relationships: {
          teams: {
            data: [
              {
                id: '1',
                type: 'teams',
              },
              {
                id: '2',
                type: 'teams',
              },
            ],
          },
        },
      },
    };
    const result = v.safeParse(JsonApiDocumentSchema, json);
    expect(result.success).toBeTruthy();
  });

  it('can typecheck a structure with an array relationship/include', () => {
    const json = {
      data: {
        id: '1',
        type: 'members',
        attributes: {
          name: 'Jigoro Kano',
          year_of_birth: 1860,
        },
        relationships: {
          teams: {
            data: [
              {
                id: '1',
                type: 'teams',
              },
              {
                id: '2',
                type: 'teams',
              },
            ],
          },
        },
      },
      included: [
        {
          id: '1',
          type: 'teams',
          attributes: { name: 'founder' },
        },
        {
          id: '2',
          type: 'teams',
          attributes: { name: '12th dan' },
        },
      ],
    };
    const result = v.safeParse(JsonApiDocumentSchema, json);
    expect(result.success).toBeTruthy();
  });
});
