<template>
  <div v-if="meeting" class="mb-4 ml-4 mr-4">
    <v-card class="pa-4" :class="{ 'unsaved-warning': dirty }" elevation="4">
      <v-card-title class="text-h6 d-flex align-center">
        <v-icon class="mr-2" color="secondary">mdi-chair-rolling</v-icon>
        Chaired Meeting Details
        <v-badge
          v-if="dirty"
          class="ml-4"
          color="orange"
          content="Unsaved changes"
        />
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
        <div class="d-flex flex-row align-start" style="gap: 24px">
          <v-textarea
            v-model="minutesEdit"
            auto-grow
            class="w-100"
            :class="{ 'unsaved-warning': dirty }"
            :disabled="saving"
            label="Minutes"
            :rows="undefined"
          />
          <div class="d-flex flex-column" style="gap: 12px; min-width: 110px">
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
        </div>
        <!-- Three columns for participants, objectives, key results -->
        <div class="d-flex flex-row mt-6" style="gap: 32px">
          <!-- Participants column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Participants</h4>
            <v-select
              v-model="selectedParticipantToAdd"
              class="mb-2"
              dense
              :disabled="saving || !availableMembers.length"
              hide-details
              item-title="label"
              item-value="id"
              :items="availableMembers"
              label="Add participant"
            />
            <v-btn
              class="mb-4"
              color="primary"
              :disabled="!selectedParticipantToAdd || saving"
              @click="addParticipant"
              >Add</v-btn
            >
            <v-list v-if="participants.length" density="compact">
              <v-list-item
                v-for="p in participants"
                :key="p.member_id"
                class="d-flex align-center"
              >
                <span>
                  {{ memberMap[p.member_id]?.first_name }}
                  {{ memberMap[p.member_id]?.last_name }}
                </span>
                <v-spacer />
                <v-btn
                  color="error"
                  :disabled="saving"
                  size="x-small"
                  title="Remove participant"
                  @click="removeParticipant(p.member_id)"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <div v-else class="text-grey">No participants</div>
          </div>
          <!-- Objectives column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Objectives</h4>
            <!-- TODO: Implement objectives association management -->
            <div class="text-grey">Coming soon</div>
          </div>
          <!-- Key Results column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Key Results</h4>
            <!-- TODO: Implement key results association management -->
            <div class="text-grey">Coming soon</div>
          </div>
        </div>
        <v-snackbar
          v-model="snackbar.show"
          :color="snackbar.color"
          timeout="4000"
        >
          {{ snackbar.text }}
        </v-snackbar>
        <!-- Warning dialog removed: no longer needed since chair icon is disabled when dirty -->
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
  import { computed, onMounted, ref, toRefs, watch } from 'vue'
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

  // Participants management
  const participants = ref([])
  const availableMembers = ref([])
  const selectedParticipantToAdd = ref(null)

  async function fetchParticipants() {
    try {
      const res = await api.get(`/meetings/${meeting.value.id}/participants`)
      participants.value = res.data
    } catch {
      participants.value = []
    }
  }
  async function fetchAvailableMembers() {
    try {
      const res = await api.get('/members')
      // Exclude already-participating members
      const participantIds = new Set(participants.value.map((p) => p.member_id))
      availableMembers.value = res.data
        .filter((m) => !participantIds.has(m.id))
        .map((m) => ({ id: m.id, label: `${m.first_name} ${m.last_name}` }))
    } catch {
      availableMembers.value = []
    }
  }
  async function addParticipant() {
    if (!selectedParticipantToAdd.value) return
    saving.value = true
    try {
      await api.post(`/meetings/${meeting.value.id}/participants`, {
        member_id: selectedParticipantToAdd.value,
      })
      await fetchParticipants()
      await fetchAvailableMembers()
      selectedParticipantToAdd.value = null
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to add participant',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
  async function removeParticipant(memberId) {
    saving.value = true
    try {
      await api.delete(`/meetings/${meeting.value.id}/participants/${memberId}`)
      await fetchParticipants()
      await fetchAvailableMembers()
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to remove participant',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }

  // Fetch participants and available members on mount and when meeting changes
  watch(
    () => meeting.value.id,
    async (newId, oldId) => {
      if (newId !== oldId) {
        await fetchParticipants()
        await fetchAvailableMembers()
      }
    },
    { immediate: true }
  )
  onMounted(() => {
    fetchParticipants()
    fetchAvailableMembers()
  })

  const leadName = computed(() => {
    const m = memberMap.value[meeting.value.lead_member_id]
    return m
      ? m.first_name + ' ' + m.last_name
      : meeting.value.lead_name || meeting.value.lead_member_id || ''
  })

  const dirty = computed(() => minutesEdit.value !== originalMinutes.value)

  defineExpose({ dirty })

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
