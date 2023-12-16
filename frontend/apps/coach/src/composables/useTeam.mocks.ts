import { HttpResponse, http } from 'msw';

export const teams = {
  data: [
    {
      type: 'teams',
      id: '1',
      attributes: {
        name: 'U15',
      },
    },
    {
      type: 'teams',
      id: '2',
      attributes: {
        name: 'U18',
      },
    },
    {
      type: 'teams',
      id: '3',
      attributes: {
        name: 'U21',
      },
    },
  ],
};

export const handlers = [
  http.get('*/v1/teams', () => {
    return HttpResponse.json(teams, { status: 200 });
  }),
];
