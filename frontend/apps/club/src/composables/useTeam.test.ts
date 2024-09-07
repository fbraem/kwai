import { describe, expect, it } from 'vitest';
import { TeamDocumentSchema, transform } from '@root/composables/useTeam';

const teamWithoutMembersJson = {
  data: {
    type: 'teams',
    id: '1',
    attributes: { name: 'U11', active: true, remark: '' },
    relationships: { team_members: { data: [] } },
  },
};

const teamWithMembersJson = {
  data: {
    type: 'teams',
    id: '1',
    attributes: { name: 'U11', active: true, remark: '' },
    relationships: {
      team_members: {
        data: [
          { type: 'team_members', id: '1' },
        ],
      },
    },
  },
  included: [{
    type: 'team_members',
    id: '1',
    attributes: { name: 'Jigoro Kano' },
    relationships: {
      nationality: {
        data: { type: 'countries', id: '1' },
      },
    },
  }, {
    type: 'countries',
    id: '1',
    attributes: { iso_2: 'JP', iso_3: 'JPN', name: 'Japan' },
  },
  ],
};

const parse = (json) => {
  const result = TeamDocumentSchema.safeParse(json);
  if (!result.success) {
    console.log(result.error);
  }
  return result;
};

describe('useTeam tests', () => {
  it('can handle a team document', () => {
    const { data: document, success } = parse(teamWithoutMembersJson);

    expect(success).toBeTruthy();
    expect(document.data.type).toEqual('teams');
    expect(document.data.id).toEqual('1');
    expect(document.data.attributes.name).toEqual('U11');
  });

  it('can handle a team document with team members', () => {
    const { data: document, success } = parse(teamWithMembersJson);

    expect(success).toBeTruthy();
    expect(document.data.type).toEqual('teams');
    expect(document).toHaveProperty('data.id', '1');
    expect(document.data.relationships.team_members.data).toHaveLength(1);
    expect(document.included).toHaveLength(2);
    expect(document).toHaveProperty('included.0.type', 'team_members');
    expect(document).toHaveProperty('included.0.id', '1');
    expect(document).toHaveProperty('included.0.attributes.name', 'Jigoro Kano');
  });

  it('can transform a document with a team', () => {
    const { data: document } = parse(teamWithoutMembersJson);

    const team = transform(document);
    expect(team).not.toBeNull();
    expect(team).toHaveProperty('id', '1');
    expect(team).toHaveProperty('name', 'U11');
    expect(team.members).toHaveLength(0);
  });

  it('can transform a document with a team and members', () => {
    const { data: document } = parse(teamWithMembersJson);
    const team = transform(document);
    expect(team).not.toBeNull();
    expect(team).toHaveProperty('id', '1');
    expect(team).toHaveProperty('name', 'U11');
    expect(team).toHaveProperty('members.0.name', 'Jigoro Kano');
    expect(team).toHaveProperty('members.0.nationality.name', 'Japan');
  });
});
