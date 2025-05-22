<template>
  <v-dialog v-model="dialogOpen" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{
          isEdit ? 'Edit Objective' : 'Add Objective'
        }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row>
            <v-col cols="7">
              <v-text-field v-model="form.title" label="Title" required />
            </v-col>
            <v-col cols="5">
              <v-select
                v-model="form.member_id"
                clearable
                item-title="label"
                item-value="id"
                :items="memberOptions"
                label="Member"
                :loading="loadingMembers"
                required
                return-object="false"
              />
            </v-col>
          </v-row>
          <v-textarea v-model="form.description" label="Description" />
          <v-text-field
            v-model="form.measurable_target"
            label="Measurable Target"
          />
          <v-row>
            <v-col cols="6">
              <v-select
                v-model="form.priority"
                :items="priorityOptions"
                label="Priority"
                :loading="loadingEnums"
                required
              />
            </v-col>
            <v-col cols="6">
              <v-select
                v-model="form.status"
                :items="statusOptions"
                label="Status"
                :loading="loadingEnums"
                required
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4">
              <v-text-field
                v-model="form.progress"
                label="Progress (%)"
                max="100"
                min="0"
                type="number"
              />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="form.start_date"
                label="Start Date"
                required
                type="date"
              />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="form.end_date"
                label="End Date"
                required
                type="date"
              />
            </v-col>
          </v-row>
          <v-select
            v-model="form.parent_id"
            clearable
            item-title="label"
            item-value="id"
            :items="parentOptions"
            label="Parent Objective"
            :loading="loadingParents"
            return-object="false"
          />
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
    objectiveId: { type: [Number, String], default: null },
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
    description: '',
    priority: '',
    status: '',
    measurable_target: '',
    progress: 0,
    start_date: '',
    end_date: '',
    parent_id: '',
    member_id: '',
  })
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.objectiveId)

  const priorityOptions = ref([])
  const statusOptions = ref([])
  const parentOptions = ref([])
  const memberOptions = ref([])
  const loadingEnums = ref(false)
  const loadingParents = ref(false)
  const loadingMembers = ref(false)
  const saving = ref(false)

  watch(
    () => props.open,
    async (val) => {
      if (val) {
        loadingEnums.value = true
        loadingParents.value = true
        loadingMembers.value = true
        try {
          const [priorities, statuses, parents, members] = await Promise.all([
            api.get('/objective-enums/priorities'),
            api.get('/objective-enums/statuses'),
            api.get('/objectives'),
            api.get('/members'),
          ])
          priorityOptions.value = priorities.data
          statusOptions.value = statuses.data
          parentOptions.value = parents.data.map((o) => ({
            id: o.id,
            label: o.title,
          }))
          memberOptions.value = members.data.map((m) => ({
            id: m.id,
            label: `${m.first_name} ${m.last_name}`,
          }))
        } catch {
          priorityOptions.value = []
          statusOptions.value = []
          parentOptions.value = []
          memberOptions.value = []
        } finally {
          loadingEnums.value = false
          loadingParents.value = false
          loadingMembers.value = false
        }
        if (props.objectiveId) {
          await loadObjective()
        } else {
          resetForm()
        }
      }
    }
  )

  async function loadObjective() {
    try {
      const res = await api.get(`/objectives/${props.objectiveId}`)
      Object.assign(form.value, res.data)
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load objective: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    }
  }

  function resetForm() {
    form.value = {
      title: '',
      description: '',
      priority: '',
      status: '',
      measurable_target: '',
      progress: 0,
      start_date: '',
      end_date: '',
      parent_id: '',
      member_id: '',
    }
  }

  function validateForm() {
    if (
      !form.value.title ||
      !form.value.priority ||
      !form.value.status ||
      !form.value.start_date ||
      !form.value.end_date
    ) {
      snackbar.value = {
        show: true,
        text: 'Please fill in all required fields.',
        color: 'error',
      }
      return false
    }
    // Clamp progress
    if (form.value.progress < 0) form.value.progress = 0
    if (form.value.progress > 100) form.value.progress = 100
    return true
  }

  async function onSave() {
    if (!validateForm()) return
    saving.value = true
    try {
      let member_id = form.value.member_id
      if (typeof member_id === 'object' && member_id !== null) {
        member_id = member_id.id
      }
      member_id =
        member_id !== '' && member_id !== null && member_id !== undefined
          ? Number(member_id)
          : null
      let parent_id = form.value.parent_id
      if (typeof parent_id === 'object' && parent_id !== null) {
        parent_id = parent_id.id
      }
      parent_id =
        parent_id !== '' && parent_id !== null && parent_id !== undefined
          ? Number(parent_id)
          : null
      // Ensure date fields are in YYYY-MM-DD
      const start_date = form.value.start_date
        ? String(form.value.start_date).slice(0, 10)
        : ''
      const end_date = form.value.end_date
        ? String(form.value.end_date).slice(0, 10)
        : ''
      const payload = {
        ...form.value,
        parent_id,
        member_id,
        start_date,
        end_date,
        progress: Number(form.value.progress) || 0,
      }
      if (isEdit.value) {
        await api.put(`/objectives/${props.objectiveId}`, payload)
      } else {
        await api.post('/objectives', payload)
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
