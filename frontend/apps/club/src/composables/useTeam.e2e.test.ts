import { describe, expect, it } from 'vitest';
import { useTeam } from '@root/composables/useTeam';
import { defineComponent, toRef } from 'vue';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { flushPromises, mount } from '@vue/test-utils';

describe('useTeam e2e tests', () => {
  it('can get a team', async() => {
    const TestComponent = defineComponent({
      setup() {
        const { data: team } = useTeam(toRef('1'));
        return {
          team,
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
    const team = wrapper.vm.team;
    expect(team).toBeDefined();
    expect(team!.id).toBe('1');
  });
});
