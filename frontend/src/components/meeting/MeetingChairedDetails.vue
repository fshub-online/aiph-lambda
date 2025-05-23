<template>
  <div v-if="meeting" class="mt-4 mb-4 ml-4 mr-4">
    <v-card class="pa-4" elevation="4">
      <v-card-title class="text-h6 d-flex align-center">
        <v-icon class="mr-2" color="secondary">mdi-chair-rolling</v-icon>
        Chaired Meeting Details
      </v-card-title>
      <v-card-text>
        <div
          class="d-flex flex-row flex-wrap align-center mb-4"
          style="gap: 32px"
        >
          <div><b>Title:</b> {{ meeting.title }}</div>
          <div><b>Lead:</b> {{ leadName }}</div>
          <div><b>Date:</b> {{ meeting.date }}</div>
          <div><b>Time:</b> {{ meeting.time }}</div>
          <div><b>Duration:</b> {{ meeting.duration }} min</div>
        </div>
        <div>
          <v-textarea
            v-model="minutesEdit"
            auto-grow
            class="w-100"
            :disabled="saving"
            label="Minutes"
            rows="5"
          />
        </div>
        <div class="d-flex flex-row mt-2" style="gap: 12px">
          <v-btn
            color="primary"
            :disabled="!dirty || saving"
            :loading="saving"
            @click="saveMinutes"
            >Save</v-btn
          >
          <v-btn
            color="secondary"
            :disabled="!dirty || saving"
            @click="undoMinutes"
            >Undo</v-btn
          >
          <v-btn
            color="error"
            :disabled="!minutesEdit || saving"
            @click="clearMinutes"
            >Clear</v-btn
          >
        </div>
        <v-snackbar
          v-model="snackbar.show"
          :color="snackbar.color"
          timeout="4000"
        >
          {{ snackbar.text }}
        </v-snackbar>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
  import { computed, ref, toRefs, watch } from 'vue'
  import api from '@/api'

  const props = defineProps({
    meeting: { type: Object, required: true },
    memberMap: { type: Object, required: true },
  })
  const emit = defineEmits(['minutes-saved'])

  const { meeting, memberMap } = toRefs(props)
  const minutesEdit = ref(meeting.value?.minutes || '')
  const originalMinutes = ref(meeting.value?.minutes || '')
  const saving = ref(false)
  const snackbar = ref({ show: false, text: '', color: 'success' })

  const leadName = computed(() => {
    const m = memberMap.value[meeting.value.lead_member_id]
    return m
      ? m.first_name + ' ' + m.last_name
      : meeting.value.lead_name || meeting.value.lead_member_id || ''
  })

  const dirty = computed(() => minutesEdit.value !== originalMinutes.value)

  watch(
    () => meeting.value.id,
    async (newId, oldId) => {
      if (newId !== oldId) {
        await reloadMinutes()
      }
    }
  )

  async function reloadMinutes() {
    try {
      const res = await api.get(`/meetings/${meeting.value.id}`)
      minutesEdit.value = res.data.minutes || ''
      originalMinutes.value = res.data.minutes || ''
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to reload minutes: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    }
  }

  async function saveMinutes() {
    saving.value = true
    try {
      await api.put(`/meetings/${meeting.value.id}`, {
        minutes: minutesEdit.value,
      })
      originalMinutes.value = minutesEdit.value
      snackbar.value = { show: true, text: 'Minutes saved.', color: 'success' }
      emit('minutes-saved', minutesEdit.value)
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to save minutes: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }

  function clearMinutes() {
    minutesEdit.value = ''
  }

  function undoMinutes() {
    reloadMinutes()
  }
</script>

<style scoped>
  .w-100 {
    width: 100%;
  }
</style>
