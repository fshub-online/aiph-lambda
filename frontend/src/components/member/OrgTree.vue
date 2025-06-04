<template>
  <div class="org-tree">
    <ul class="org-tree-root">
      <org-tree-node v-if="root" :member="root" :members="membersMap" />
    </ul>
  </div>
</template>

<script setup>
  import { computed, defineProps } from 'vue'
  import OrgTreeNode from './OrgTreeNode.vue'

  const props = defineProps({
    members: {
      type: Array,
      required: true,
    },
    rootId: {
      type: Number,
      required: true,
    },
  })

  const membersMap = computed(() => {
    const map = {}
    for (const m of props.members) {
      map[m.id] = m
    }
    return map
  })

  const root = computed(() => membersMap.value[props.rootId])
</script>

<style scoped>
  .org-tree {
    display: flex;
    justify-content: center;
    margin-top: 32px;
  }
  .org-tree-root {
    padding-left: 0;
  }
</style>
