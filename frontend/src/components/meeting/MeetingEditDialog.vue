<template>
  <v-dialog v-model="dialogOpen" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{
          isEdit ? 'Edit Meeting' : 'Add Meeting'
        }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row>
            <v-col cols="8">
              <v-text-field v-model="form.title" label="Title" required />
            </v-col>
            <v-col cols="4">
              <v-select
                v-model="form.lead_member_id"
                clearable
                item-title="label"
                item-value="id"
                :items="memberOptions"
                label="Lead Member"
                :loading="loadingMembers"
                required
                return-object="false"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="form.date"
                label="Date"
                required
                type="date"
              />
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="form.time"
                label="Time"
                required
                type="time"
              />
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="form.duration"
                label="Duration (min)"
                min="0"
                type="number"
              />
            </v-col>
          </v-row>
          <v-textarea v-model="form.minutes" label="Minutes" />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('close')">Cancel</v-btn>
        <v-btn color="primary" :disabled="saving" @click="onSave">Save</v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-dialog>
</template>

<script setup>
  import { computed, defineEmits, defineProps, ref, watch } from 'vue'
  import api from '@/api'

  const props = defineProps({
    open: Boolean,
    meetingId: { type: [Number, String], default: null },
  })
  const emit = defineEmits(['close', 'saved'])

  const dialogOpen = ref(false)

  watch(
    () => props.open,
    (val) => {
      dialogOpen.value = val
    }
  )
  watch(dialogOpen, (val) => {
    if (!val) emit('close')
  })

  const form = ref({
    title: '',
    date: '',
    time: '',
    duration: '',
    minutes: '',
    lead_member_id: '',
  })
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.meetingId)

  const memberOptions = ref([])
  const loadingMembers = ref(false)
  const saving = ref(false)

  watch(
    () => props.open,
    async (val) => {
      if (val) {
        loadingMembers.value = true
        try {
          const members = await api.get('/members')
          memberOptions.value = members.data.map((m) => ({
            id: m.id,
            label: `${m.first_name} ${m.last_name}`,
          }))
        } catch {
          memberOptions.value = []
        } finally {
          loadingMembers.value = false
        }
        if (props.meetingId) {
          await loadMeeting()
        } else {
          resetForm()
        }
      }
    }
  )

  async function loadMeeting() {
    try {
      const res = await api.get(`/meetings/${props.meetingId}`)
      Object.assign(form.value, res.data)
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load meeting: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    }
  }

  function resetForm() {
    form.value = {
      title: '',
      date: '',
      time: '',
      duration: '',
      minutes: '',
      lead_member_id: '',
    }
  }

  function validateForm() {
    if (!form.value.title || !form.value.date || !form.value.time) {
      snackbar.value = {
        show: true,
        text: 'Please fill in all required fields.',
        color: 'error',
      }
      return false
    }
    if (form.value.duration && form.value.duration < 0) form.value.duration = 0
    return true
  }

  async function onSave() {
    if (!validateForm()) return
    saving.value = true
    try {
      let lead_member_id = form.value.lead_member_id
      if (typeof lead_member_id === 'object' && lead_member_id !== null) {
        lead_member_id = lead_member_id.id
      }
      lead_member_id =
        lead_member_id !== '' &&
        lead_member_id !== null &&
        lead_member_id !== undefined
          ? Number(lead_member_id)
          : null
      // Ensure date and time are null if empty string
      const date =
        form.value.date && form.value.date !== '' ? form.value.date : null
      const time =
        form.value.time && form.value.time !== '' ? form.value.time : null
      const payload = {
        ...form.value,
        date,
        time,
        lead_member_id,
        duration: form.value.duration ? Number(form.value.duration) : null,
      }
      if (isEdit.value) {
        await api.put(`/meetings/${props.meetingId}`, payload)
      } else {
        await api.post('/meetings', payload)
      }
      emit('saved')
      emit('close')
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Save failed: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    } finally {
      saving.value = false
    }
  }
</script>
