<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-alert
          v-for="msg in filteredSortedMessages"
          :key="msg.id"
          class="mb-4 elevation-4"
          :type="priorityType(msg.priority)"
        >
          <div class="text-h6">{{ msg.title }}</div>
          <div>{{ msg.message }}</div>
          <div class="text-caption grey--text">From: {{ msg.display_start }} To: {{ msg.display_end }}</div>
        </v-alert>
        <div v-if="filteredSortedMessages.length === 0" class="text-center text-grey">No messages to display.</div>
      </v-col>
    </v-row>
  </v-container>
  <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
    {{ snackbar.text }}
  </v-snackbar>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import api from '@/api'

  const messages = ref([])
  const priorities = ref([])
  const today = new Date()

  const snackbar = ref({ show: false, text: '', color: 'error' })

  function priorityType (priority) {
    // Map backend priorities to Vuetify VAlert types
    switch (priority) {
      case priorities.value[0]: return 'success' // Top
      case priorities.value[1]: return 'warning' // High
      case priorities.value[2]: return 'info' // Medium
      case priorities.value[3]: return 'error' // Low
      default: return 'info'
    }
  }

  const filteredSortedMessages = computed(() => {
    return messages.value
      .filter(msg => {
        const start = msg.display_start ? new Date(msg.display_start) : null
        const end = msg.display_end ? new Date(msg.display_end) : null
        return (
          (!start || today >= start) &&
          (!end || today <= end)
        )
      })
      .sort((a, b) => {
        // Sort by priority order from backend
        const pA = priorities.value.indexOf(a.priority)
        const pB = priorities.value.indexOf(b.priority)
        if (pA !== pB) return pA - pB
        // Then by display_start descending
        const dA = a.display_start ? new Date(a.display_start) : new Date(0)
        const dB = b.display_start ? new Date(b.display_start) : new Date(0)
        return dB - dA
      })
  })

  onMounted(async () => {
    try {
      // Load priorities first
      const prioRes = await api.get('/message-enums/priorities')
      priorities.value = prioRes.data
    } catch (e) {
      snackbar.value = {
        show: true,
        text: e?.response?.data?.detail || e.message || 'Failed to load priorities',
        color: 'error',
      }
      priorities.value = []
    }
    try {
      const res = await api.get('/messages')
      messages.value = res.data
    } catch (e) {
      snackbar.value = {
        show: true,
        text: e?.response?.data?.detail || e.message || 'Failed to load messages',
        color: 'error',
      }
      messages.value = []
    }
  })

  window.addEventListener('show-auth-warning', () => {
    snackbar.value = {
      show: true,
      text: 'You must be authenticated to access that page.',
      color: 'warning',
    }
  })
</script>
