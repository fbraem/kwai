import { describe, expect, it, vi } from 'vitest';
import { useTeam } from '@root/composables/useTeam';
import { defineComponent, toRef } from 'vue';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { mount } from '@vue/test-utils';

describe('useTeam e2e tests', () => {
  it('can get a team', async() => {
    const TestComponent = defineComponent({
      setup() {
        return useTeam(toRef('1'));
      },
      template: '<span>Test Component</span>',
    });
    const wrapper = mount(TestComponent, {
      global: {
        plugins: [VueQueryPlugin],
      },
    });
    await vi.waitFor(() => {
      expect(wrapper.vm.isPending).toBeFalsy();
    }, { timeout: 1000 });
    const team = wrapper.vm.data;
    expect(team).toBeDefined();
    expect(team!.id).toBe('1');
  });
});
