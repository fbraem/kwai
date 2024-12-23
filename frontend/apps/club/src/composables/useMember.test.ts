import { describe, expect, it } from 'vitest';
import { MemberDocumentSchema } from '@root/composables/useMember';

const memberJson = {
  data: {
    type: 'members',
    id: '1',
    attributes: {
      license_number: '123456',
      license_end_date: '2024-31-01',
      active: true,
      competition: false,
      remark: '',
    },
    relationships: {
      person: {
        data: {
          type: 'persons',
          id: '1',
        },
      },
    },
  },
  included: [
    {
      type: 'persons',
      id: '1',
      attributes: {
        first_name: 'Jigoro',
        last_name: 'Kano',
        gender: 1,
        birthdate: '18',
        remark: '',
      },
      relationships: {
        contact: {
          data: {
            type: 'contacts',
            id: '1',
          },
        },
        nationality: {
          data: {
            type: 'countries',
            id: '1',
          },
        },
      },
    },
    {
      type: 'contacts',
      id: '1',
      attributes: {
        emails: [],
        tel: '',
        mobile: '',
        address: '',
        postal_code: '',
        city: '',
        county: '',
        remark: '',
      },
      relationships: {
        country: {
          data: {
            type: 'countries',
            id: '1',
          },
        },
      },
    },
    {
      type: 'countries',
      id: '1',
      attributes: {
        iso_2: 'JP',
        iso_3: 'JPN',
        name: 'Japan',
      },
    },
  ],
};

const parse = (json: unknown) => {
  const result = MemberDocumentSchema.safeParse(json);
  if (!result.success) {
    console.log(result.error);
  }
  return result;
};

describe('useMember tests', () => {
  it('can handle a member document', () => {
    const { data: document, success } = parse(memberJson);
    expect(success).toBeTruthy();
    expect(document).toHaveProperty('data.type', 'members');
  });
  it('can handle a member array document', () => {
    const { data: document, success } = parse({ data: [memberJson.data] });
    expect(success).toBeTruthy();
    expect(document!.data).toHaveLength(1);
    expect(document).toHaveProperty('data.0.type', 'members');
  });
});
