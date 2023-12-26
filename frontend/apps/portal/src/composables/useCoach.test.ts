import { handlers } from './useCoach.mocks';
import { setupServer } from 'msw/node';
import { describe, beforeAll, afterAll, afterEach, it, expect } from 'vitest';
import { useCoaches } from '@root/composables/useCoach';
import type { Coach } from '@root/composables/useCoach';
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

describe('can handle coaches', () => {
  it('can get coaches', async() => {
    const TestComponent = defineComponent({
      setup() {
        const { data: coaches } = useCoaches();
        return {
          coaches,
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
    const coaches: Coach[]|undefined = wrapper.vm.coaches;
    expect(coaches).toBeDefined();
    expect(coaches).toHaveLength(2);
    expect(coaches!.map(coach => coach.id)).toEqual(['1', '2']);
    expect(coaches![0].name).toEqual('Jigoro Kano');
  });
});
