import { handlers } from './useTeam.mocks';
import { setupServer } from 'msw/node';
import { describe, beforeAll, afterAll, afterEach, it, expect } from 'vitest';
import { useTeams } from '@root/composables/useTeam';
import type { Team } from '@root/composables/useTeam';
import { defineComponent } from 'vue';
import { flushPromises, mount } from '@vue/test-utils';
import { VueQueryPlugin } from '@tanstack/vue-query';

const server = setupServer(...handlers);
// Start server before all tests
beforeAll(() => server.listen());
//  Close server after all tests
afterAll(() => server.close());
// Reset handlers after each test `important for test isolation`
afterEach(() => server.resetHandlers());

describe('can handle teams', () => {
  it('can get teams', async() => {
    const TestComponent = defineComponent({
      setup() {
        const { data: teams } = useTeams();
        return {
          teams,
        };
      },
      template: '<span>Test Component</span>',
    });
    const wrapper = mount(TestComponent, {
      global: {
        plugins: [VueQueryPlugin],
      },
    });
    await flushPromises();
    const teams: Team[]|undefined = wrapper.vm.teams;
    expect(teams).toBeDefined();
    expect(teams).toHaveLength(3);
    expect(teams!.map(team => team.id)).toEqual(['1', '2', '3']);
    expect(teams![0].name).toEqual('U15');
  });
});
