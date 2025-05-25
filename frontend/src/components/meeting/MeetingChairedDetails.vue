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
          style="gap: 12px"
        >
          <div><b>Title:</b> {{ meeting.title }}</div>
          <div><b>Lead:</b> {{ leadName }}</div>
          <div><b>Date:</b> {{ meeting.date }}</div>
          <div><b>Time:</b> {{ meeting.time }}</div>
          <div><b>Duration:</b> {{ meeting.duration }} min</div>
        </div>
        <div class="d-flex flex-row align-start" style="gap: 8px">
          <v-textarea
            v-model="minutesEdit"
            auto-grow
            :class="{ 'unsaved-warning': dirty }"
            density="compact"
            :disabled="saving"
            label="Minutes"
            rows="7"
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
        <div class="d-flex flex-row mt-0" style="gap: 32px">
          <!-- Participants column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Participants</h4>
            <!-- List of participants as comma-separated, with remove icon -->
            <div v-if="participants.length">
              <span v-for="p in participants" :key="p.member_id" class="mr-2">
                <span>
                  {{ memberMap[p.member_id]?.first_name }}
                  {{ memberMap[p.member_id]?.last_name }}
                </span>
                <v-btn
                  class="ml-1 mr-1"
                  color="error"
                  :disabled="saving"
                  icon
                  size="xx-small"
                  style="vertical-align: middle"
                  title="Remove participant"
                  @click="removeParticipant(p.member_id)"
                >
                  <v-icon small>mdi-close</v-icon>
                </v-btn>
              </span>
            </div>
            <div v-else class="text-grey">No participants</div>
            <!-- Dropdown to add participant -->
            <div
              class="d-flex flex-row align-center mb-2 mt-2"
              style="gap: 8px"
            >
              <v-select
                v-model="selectedParticipantToAdd"
                dense
                :disabled="saving || !availableMembers.length"
                hide-details
                item-title="label"
                item-value="id"
                :items="availableMembers"
                label="Add participant"
                style="flex: 1"
              />
              <v-btn
                color="primary"
                :disabled="!selectedParticipantToAdd || saving"
                @click="addParticipant"
              >
                Add
              </v-btn>
            </div>
          </div>
          <!-- Objectives column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Objectives</h4>
            <!-- List of linked objectives with notes -->
            <div v-if="objectives.length">
              <div
                v-for="obj in objectives"
                :key="obj.objective_id"
                class="mb-3"
                style=""
              >
                <div class="d-flex align-center mb-1">
                  <span class="">
                    {{ objectiveMap[obj.objective_id]?.title }}
                  </span>
                  <v-btn
                    class="ml-1"
                    color="error"
                    icon
                    size="xx-small"
                    title="Remove objective"
                    @click="removeObjective(obj.objective_id)"
                  >
                    <v-icon small>mdi-close</v-icon>
                  </v-btn>
                </div>
                <div class="d-flex flex-row align-start" style="gap: 8px">
                  <v-textarea
                    v-model="obj._noteEdit"
                    auto-grow
                    class="mb-1"
                    dense
                    :disabled="saving"
                    label="Note"
                    style="flex: 1"
                  />
                  <div class="d-flex flex-column align-start button-group-top">
                    <v-btn
                      class="note-action-btn"
                      color="primary"
                      :disabled="saving || !objectiveNoteDirty(obj)"
                      :loading="obj._noteSaving"
                      @click="saveObjectiveNote(obj)"
                    >
                      Save
                    </v-btn>
                    <v-btn
                      class="note-action-btn"
                      color="secondary"
                      :disabled="saving || !objectiveNoteDirty(obj)"
                      @click="undoObjectiveNote(obj)"
                    >
                      Undo
                    </v-btn>
                    <v-btn
                      class="note-action-btn"
                      color="error"
                      :disabled="
                        saving || !(obj._noteEdit && obj._noteEdit.length)
                      "
                      @click="clearObjectiveNote(obj)"
                    >
                      Clear
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-grey">No objectives</div>
            <!-- Dropdown to add objective -->
            <div
              class="d-flex flex-row align-center mb-2 mt-2"
              style="gap: 8px"
            >
              <v-select
                v-model="selectedObjectiveToAdd"
                dense
                :disabled="saving || !availableObjectives.length"
                hide-details
                item-title="label"
                item-value="id"
                :items="availableObjectives"
                label="Add objective"
                style="flex: 1"
              />
              <v-btn
                color="primary"
                :disabled="!selectedObjectiveToAdd || saving"
                @click="addObjective"
              >
                Add
              </v-btn>
            </div>
          </div>
          <!-- Key Results column -->
          <div style="flex: 1; min-width: 220px">
            <h4 class="mb-2">Key Results</h4>
            <!-- List of linked key results with notes -->
            <div v-if="keyResults.length">
              <div
                v-for="kr in keyResults"
                :key="kr.key_result_id"
                class="mb-3"
              >
                <div class="d-flex align-center mb-1">
                  <span class="">
                    {{ keyResultMap[kr.key_result_id]?.title }}
                  </span>
                  <v-btn
                    class="ml-2"
                    color="error"
                    icon
                    size="xx-small"
                    title="Remove key result"
                    @click="removeKeyResult(kr.key_result_id)"
                  >
                    <v-icon small>mdi-close</v-icon>
                  </v-btn>
                </div>
                <div class="d-flex flex-row align-start" style="gap: 8px">
                  <v-textarea
                    v-model="kr._noteEdit"
                    auto-grow
                    dense
                    :disabled="saving"
                    label="Note"
                    style="flex: 1"
                  />
                  <div class="d-flex flex-column align-start button-group-top">
                    <v-btn
                      class="note-action-btn"
                      color="primary"
                      :disabled="saving || !keyResultNoteDirty(kr)"
                      :loading="kr._noteSaving"
                      @click="saveKeyResultNote(kr)"
                    >
                      Save
                    </v-btn>
                    <v-btn
                      class="note-action-btn"
                      color="secondary"
                      :disabled="saving || !keyResultNoteDirty(kr)"
                      @click="undoKeyResultNote(kr)"
                    >
                      Undo
                    </v-btn>
                    <v-btn
                      class="note-action-btn"
                      color="error"
                      :disabled="
                        saving || !(kr._noteEdit && kr._noteEdit.length)
                      "
                      @click="clearKeyResultNote(kr)"
                    >
                      Clear
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-grey">No key results</div>
            <!-- Dropdown to add key result -->
            <div
              class="d-flex flex-row align-center mb-2 mt-2"
              style="gap: 8px"
            >
              <v-select
                v-model="selectedKeyResultToAdd"
                dense
                :disabled="saving || !availableKeyResults.length"
                hide-details
                item-title="label"
                item-value="id"
                :items="availableKeyResults"
                label="Add key result"
                style="flex: 1"
              />
              <v-btn
                color="primary"
                :disabled="!selectedKeyResultToAdd || saving"
                @click="addKeyResult"
              >
                Add
              </v-btn>
            </div>
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
      // Exclude already-participating members and the lead member
      const participantIds = new Set(participants.value.map((p) => p.member_id))
      const leadId = meeting.value.lead_member_id
      availableMembers.value = res.data
        .filter((m) => !participantIds.has(m.id) && m.id !== leadId)
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

  // Objectives management
  const objectives = ref([])
  const availableObjectives = ref([])
  const selectedObjectiveToAdd = ref(null)
  const objectiveMap = ref({})

  async function fetchObjectives() {
    try {
      const res = await api.get(`/meetings/${meeting.value.id}/objectives`)
      objectives.value = res.data
    } catch {
      objectives.value = []
    }
  }
  async function fetchAvailableObjectives() {
    try {
      const [allObjRes, linkedObjRes] = await Promise.all([
        api.get('/objectives'),
        api.get(`/meetings/${meeting.value.id}/objectives`),
      ])
      const linkedIds = new Set(linkedObjRes.data.map((o) => o.objective_id))
      availableObjectives.value = allObjRes.data
        .filter((o) => !linkedIds.has(o.id))
        .map((o) => ({ id: o.id, label: o.title }))
      // Build objectiveMap for display
      const map = {}
      for (const o of allObjRes.data) map[o.id] = o
      objectiveMap.value = map
    } catch {
      availableObjectives.value = []
      objectiveMap.value = {}
    }
  }
  async function addObjective() {
    if (!selectedObjectiveToAdd.value) return
    saving.value = true
    try {
      await api.post(`/meetings/${meeting.value.id}/objectives`, {
        objective_id: selectedObjectiveToAdd.value,
        note: '',
      })
      await fetchObjectives()
      await fetchAvailableObjectives()
      selectedObjectiveToAdd.value = null
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to add objective',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
  async function removeObjective(objectiveId) {
    saving.value = true
    try {
      await api.delete(
        `/meetings/${meeting.value.id}/objectives/${objectiveId}`
      )
      await fetchObjectives()
      await fetchAvailableObjectives()
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to remove objective',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
  function objectiveNoteDirty(obj) {
    return (obj._noteEdit ?? obj.note ?? '') !== (obj.note ?? '')
  }
  function undoObjectiveNote(obj) {
    obj._noteEdit = obj.note || ''
  }
  function clearObjectiveNote(obj) {
    obj._noteEdit = ''
  }
  async function saveObjectiveNote(obj) {
    obj._noteSaving = true
    saving.value = true
    try {
      await api.put(
        `/meetings/${meeting.value.id}/objectives/${obj.objective_id}`,
        {
          note: obj._noteEdit,
          objective_id: obj.objective_id, // Added to match backend schema
        }
      )
      obj.note = obj._noteEdit
      snackbar.value = {
        show: true,
        text: 'Note saved.',
        color: 'success',
      }
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to save note',
        color: 'error',
      }
    } finally {
      obj._noteSaving = false
      saving.value = false
    }
  }
  // Patch: initialize _noteEdit for each objective on fetch
  watch(
    objectives,
    (objs) => {
      for (const obj of objs) {
        if (obj._noteEdit === undefined) obj._noteEdit = obj.note || ''
      }
    },
    { immediate: true }
  )

  // Key Results management
  const keyResults = ref([])
  const availableKeyResults = ref([])
  const selectedKeyResultToAdd = ref(null)
  const keyResultMap = ref({})

  async function fetchKeyResults() {
    try {
      const res = await api.get(`/meetings/${meeting.value.id}/key-results`)
      keyResults.value = res.data
    } catch {
      keyResults.value = []
    }
  }
  async function fetchAvailableKeyResults() {
    try {
      const [allKRRes, linkedKRRes] = await Promise.all([
        api.get('/key-results'),
        api.get(`/meetings/${meeting.value.id}/key-results`),
      ])
      const linkedIds = new Set(linkedKRRes.data.map((kr) => kr.key_result_id))
      availableKeyResults.value = allKRRes.data
        .filter((kr) => !linkedIds.has(kr.id))
        .map((kr) => ({ id: kr.id, label: kr.title }))
      // Build keyResultMap for display
      const map = {}
      for (const kr of allKRRes.data) map[kr.id] = kr
      keyResultMap.value = map
    } catch {
      availableKeyResults.value = []
      keyResultMap.value = {}
    }
  }
  async function addKeyResult() {
    if (!selectedKeyResultToAdd.value) return
    saving.value = true
    try {
      await api.post(`/meetings/${meeting.value.id}/key-results`, {
        key_result_id: selectedKeyResultToAdd.value,
        note: '',
      })
      await fetchKeyResults()
      await fetchAvailableKeyResults()
      selectedKeyResultToAdd.value = null
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to add key result',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
  async function removeKeyResult(keyResultId) {
    saving.value = true
    try {
      await api.delete(
        `/meetings/${meeting.value.id}/key-results/${keyResultId}`
      )
      await fetchKeyResults()
      await fetchAvailableKeyResults()
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to remove key result',
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
  function keyResultNoteDirty(kr) {
    return (kr._noteEdit ?? kr.note ?? '') !== (kr.note ?? '')
  }
  function undoKeyResultNote(kr) {
    kr._noteEdit = kr.note || ''
  }
  function clearKeyResultNote(kr) {
    kr._noteEdit = ''
  }
  async function saveKeyResultNote(kr) {
    kr._noteSaving = true
    saving.value = true
    try {
      await api.put(
        `/meetings/${meeting.value.id}/key-results/${kr.key_result_id}`,
        {
          note: kr._noteEdit,
          key_result_id: kr.key_result_id,
        }
      )
      kr.note = kr._noteEdit
      snackbar.value = {
        show: true,
        text: 'Note saved.',
        color: 'success',
      }
    } catch {
      snackbar.value = {
        show: true,
        text: 'Failed to save note',
        color: 'error',
      }
    } finally {
      kr._noteSaving = false
      saving.value = false
    }
  }
  // Patch: initialize _noteEdit for each key result on fetch
  watch(
    keyResults,
    (krs) => {
      for (const kr of krs) {
        if (kr._noteEdit === undefined) kr._noteEdit = kr.note || ''
      }
    },
    { immediate: true }
  )

  // Fetch participants, available members, objectives, and available objectives on mount and when meeting changes
  watch(
    () => meeting.value.id,
    async (newId, oldId) => {
      if (newId !== oldId) {
        await fetchParticipants()
        await fetchAvailableMembers()
        await fetchObjectives()
        await fetchAvailableObjectives()
        await fetchKeyResults()
        await fetchAvailableKeyResults()
      }
    },
    { immediate: true }
  )
  onMounted(() => {
    fetchParticipants()
    fetchAvailableMembers()
    fetchObjectives()
    fetchAvailableObjectives()
    fetchKeyResults()
    fetchAvailableKeyResults()
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
  .note-btn {
    min-width: 80px;
    height: 40px;
    font-size: 1rem;
    padding: 0 12px;
    box-sizing: border-box;
  }
  .objective-btn-col,
  .keyresult-btn-col {
    align-items: stretch !important;
    align-self: flex-start !important;
    height: 100%;
  }
  .button-group-top {
    align-items: flex-start;
    gap: 8px;
  }
  .note-action-btn {
    min-width: 80px;
    height: 36px;
    font-size: 0.875rem;
    padding: 0 8px;
    box-sizing: border-box;
  }
</style>
