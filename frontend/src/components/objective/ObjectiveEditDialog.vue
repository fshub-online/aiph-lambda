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
          <v-text-field v-model="form.title" label="Title" required />
          <v-textarea v-model="form.description" label="Description" />
          <v-select
            v-model="form.priority"
            :items="priorityOptions"
            label="Priority"
            :loading="loadingEnums"
            required
          />
          <v-select
            v-model="form.status"
            :items="statusOptions"
            label="Status"
            :loading="loadingEnums"
            required
          />
          <v-text-field
            v-model="form.measurable_target"
            label="Measurable Target"
          />
          <v-text-field
            v-model="form.progress"
            label="Progress (%)"
            max="100"
            min="0"
            type="number"
          />
          <v-text-field
            v-model="form.start_date"
            label="Start Date"
            required
            type="date"
          />
          <v-text-field
            v-model="form.end_date"
            label="End Date"
            required
            type="date"
          />
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
        <v-btn color="primary" @click="onSave">Save</v-btn>
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
  })
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.objectiveId)

  const priorityOptions = ref([])
  const statusOptions = ref([])
  const parentOptions = ref([])
  const loadingEnums = ref(false)
  const loadingParents = ref(false)

  watch(
    () => props.open,
    async (val) => {
      if (val) {
        loadingEnums.value = true
        loadingParents.value = true
        try {
          const [priorities, statuses, parents] = await Promise.all([
            api.get('/objective-priorities'),
            api.get('/objective-statuses'),
            api.get('/objectives'),
          ])
          priorityOptions.value = priorities.data
          statusOptions.value = statuses.data
          parentOptions.value = parents.data.map((o) => ({
            id: o.id,
            label: o.title,
          }))
        } catch {
          priorityOptions.value = []
          statusOptions.value = []
          parentOptions.value = []
        } finally {
          loadingEnums.value = false
          loadingParents.value = false
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
    }
  }

  async function onSave() {
    try {
      const payload = {
        ...form.value,
        parent_id: form.value.parent_id ? Number(form.value.parent_id) : null,
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
    }
  }
</script>
