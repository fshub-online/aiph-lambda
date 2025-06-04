<template>
  <li class="org-tree-node">
    <div class="member-box">
      <span class="member-name"
        >{{ member.first_name }} {{ member.last_name }}</span
      >
      <span v-if="member.position" class="member-position"
        >({{ member.position }})</span
      >
    </div>
    <div v-if="subordinates.length" class="org-tree-connector">
      <span class="vertical-line"></span>
      <div class="horizontal-lines">
        <span
          v-for="sub in subordinates"
          :key="sub.id"
          class="horizontal-line"
        ></span>
      </div>
    </div>
    <ul v-if="subordinates.length" class="org-tree-children">
      <org-tree-node
        v-for="sub in subordinates"
        :key="sub.id"
        :member="sub"
        :members="members"
      />
    </ul>
  </li>
</template>

<script setup>
  import { computed, defineProps } from 'vue'

  const props = defineProps({
    member: { type: Object, required: true },
    members: { type: Object, required: true },
  })

  const subordinates = computed(() => {
    return Object.values(props.members).filter(
      (m) => m.supervisor_id === props.member.id
    )
  })
</script>

<style scoped>
  .org-tree-node {
    list-style: none;
    text-align: center;
    position: relative;
    padding-top: 32px;
  }
  .member-box {
    display: inline-block;
    background: #fff;
    border: 2px solid #1976d2;
    border-radius: 8px;
    padding: 12px 24px;
    box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
    font-weight: 500;
    min-width: 160px;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
  }
  .member-name {
    font-size: 1.1em;
  }
  .member-position {
    color: #888;
    font-size: 0.95em;
    margin-left: 6px;
  }
  .org-tree-children {
    display: flex;
    justify-content: center;
    gap: 32px;
    padding-left: 0;
    margin-top: 16px;
  }
  .org-tree-connector {
    position: relative;
    height: 32px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .vertical-line {
    width: 2px;
    height: 16px;
    background: #1976d2;
    display: block;
    margin: 0 auto;
  }
  .horizontal-lines {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    position: relative;
    top: 0;
  }
  .horizontal-line {
    height: 2px;
    background: #1976d2;
    flex: 1;
    margin: 0 8px;
  }
</style>
