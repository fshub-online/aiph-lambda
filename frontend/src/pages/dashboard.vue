<template>
  <v-container class="py-8">
    <h1>Dashboard</h1>
    <div v-if="loading">Loading organization tree...</div>
    <div v-else-if="error" class="text-error">{{ error }}</div>
    <div v-else>
      <OrgD3Tree
        v-if="orgTree.length && topManager"
        :height="600"
        :members="orgTree"
        :root-id="topManager.id"
        :width="1000"
      />
    </div>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import api from '@/api'
  import OrgD3Tree from '@/components/member/OrgD3Tree.vue'

  const user = ref(null)
  const member = ref(null)
  const topManager = ref(null)
  const orgTree = ref([])
  const loading = ref(true)
  const error = ref('')

  onMounted(async () => {
    try {
      // 1. Get current user
      const userRes = await api.get('/oauth/me')
      user.value = userRes.data
      // 2. Get member for user
      const memberRes = await api.get(`/members/by-user/${user.value.id}`)
      member.value = memberRes.data
      // 3. Get top manager for member
      const topManagerRes = await api.get(
        `/members/${member.value.id}/top-manager`
      )
      topManager.value = topManagerRes.data
      // 4. Get org tree for top manager
      const orgTreeRes = await api.get(
        `/members/${topManager.value.id}/org-tree`
      )
      orgTree.value = orgTreeRes.data
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message || String(e)
    } finally {
      loading.value = false
    }
  })
</script>
