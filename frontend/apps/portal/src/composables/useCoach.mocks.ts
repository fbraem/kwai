import { HttpResponse, http } from 'msw';

export const teams = {
  data: [
    {
      type: 'coaches',
      id: '1',
      attributes: {
        name: 'Jigoro Kano',
      },
    },
    {
      type: 'coaches',
      id: '2',
      attributes: {
        name: 'Ichiro Abe',
      },
    },
  ],
};

export const handlers = [
  http.get('*/v1/trainings/coaches', () => {
    return HttpResponse.json(teams, { status: 200 });
  }),
];
