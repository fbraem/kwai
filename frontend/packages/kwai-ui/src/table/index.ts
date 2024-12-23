import { h, defineComponent, VNodeChild } from 'vue';

export const KwaiTableColumn = defineComponent({
  setup(props, { slots }) {
    return () => h(
      'th',
      {
        class: 'px-6 py-3',
        scope: 'col',
      },
      slots.default?.() ?? []
    );
  },
});

export const KwaiTableHead = defineComponent({
  setup(props, { slots }) {
    return () => h(
      'thead',
      { class: 'text-xs text-gray-700 uppercase bg-primary-100' },
      [h('tr', {}, slots.default?.() ?? [])]
    );
  },
});

export const KwaiTableBody = defineComponent({
  setup(props, { slots }) {
    return () => h(
      'tbody',
      { class: 'divide-y divide-primary-100' },
      slots.default?.() ?? []
    );
  },
});

export const KwaiTableCell = defineComponent({
  setup(props, { slots }) {
    return () => h(
      'td',
      { class: 'px-6 py-3' },
      slots.default?.() ?? []
    );
  },
});

export const KwaiTable = defineComponent({
  setup(props, { slots }) {
    const children: VNodeChild[] = [];

    // When there is a header slot, we pass it as the default slot
    // for the KwaiTableHead component.
    if (slots.header) {
      children.push(h(
        KwaiTableHead,
        {},
        { default: () => slots.header!() }
      ));
    }

    // When there is body slot, we pass it as the default slot
    // for the KwaiTableBody component.
    if (slots.body) {
      children.push(h(
        KwaiTableBody,
        {},
        { default: () => slots.body!() }
      ));
    }

    // The default slot is part of our children.
    if (slots.default) {
      children.push(slots.default());
    }

    return () => {
      return h(
        'table',
        { class: 'w-full text-left' },
        children
      );
    };
  },
});
