<template>
  <v-dialog v-model="dialogOpen" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{
          isEdit ? 'Edit Key Result' : 'Add Key Result'
        }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-text-field v-model="form.title" label="Title" required />
          <v-textarea v-model="form.description" label="Description" />
          <v-text-field
            v-model="form.value_definition"
            label="Value Definition"
            required
          />
          <v-text-field v-model="form.unit" label="Unit" required />
          <v-text-field
            v-model="form.start_value"
            label="Start Value"
            required
            type="number"
          />
          <v-text-field
            v-model="form.current_value"
            label="Current Value"
            required
            type="number"
          />
          <v-text-field
            v-model="form.target_value"
            label="Target Value"
            required
            type="number"
          />
          <v-select
            v-model="form.status"
            :items="statusOptions"
            label="Status"
            :loading="loadingEnums"
            required
          />
          <v-select
            v-model="form.priority"
            :items="priorityOptions"
            label="Priority"
            :loading="loadingEnums"
            required
          />
          <v-select
            v-model="form.complexity"
            :items="complexityOptions"
            label="Complexity"
            :loading="loadingEnums"
            required
          />
          <v-text-field
            v-model="form.start_date"
            label="Start Date"
            type="date"
          />
          <v-text-field v-model="form.end_date" label="End Date" type="date" />
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
          <v-select
            v-model="form.objective_id"
            clearable
            item-title="label"
            item-value="id"
            :items="objectiveOptions"
            label="Objective (optional)"
            :loading="loadingObjectives"
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
    keyResultId: { type: [Number, String], default: null },
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
    value_definition: '',
    unit: '',
    start_value: 0,
    current_value: 0,
    target_value: 0,
    status: '',
    priority: '',
    complexity: '',
    start_date: '',
    end_date: '',
    member_id: '',
    objective_id: '',
  })
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.keyResultId)

  const statusOptions = ref([])
  const priorityOptions = ref([])
  const complexityOptions = ref([])
  const memberOptions = ref([])
  const objectiveOptions = ref([])
  const loadingEnums = ref(false)
  const loadingMembers = ref(false)
  const loadingObjectives = ref(false)

  watch(
    () => props.open,
    async (val) => {
      if (val) {
        loadingEnums.value = true
        loadingMembers.value = true
        loadingObjectives.value = true
        try {
          const [statuses, priorities, complexities, members, objectives] =
            await Promise.all([
              api.get('/key-result-statuses'),
              api.get('/key-result-priorities'),
              api.get('/key-result-complexities'),
              api.get('/members'),
              api.get('/objectives'),
            ])
          statusOptions.value = statuses.data
          priorityOptions.value = priorities.data
          complexityOptions.value = complexities.data
          memberOptions.value = members.data.map((m) => ({
            id: m.id,
            label: `${m.first_name} ${m.last_name}`,
          }))
          objectiveOptions.value = objectives.data.map((o) => ({
            id: o.id,
            label: o.title,
          }))
        } catch {
          statusOptions.value = []
          priorityOptions.value = []
          complexityOptions.value = []
          memberOptions.value = []
          objectiveOptions.value = []
        } finally {
          loadingEnums.value = false
          loadingMembers.value = false
          loadingObjectives.value = false
        }
        if (props.keyResultId) {
          await loadKeyResult()
        } else {
          resetForm()
        }
      }
    }
  )

  async function loadKeyResult() {
    try {
      const res = await api.get(`/key-results/${props.keyResultId}`)
      Object.assign(form.value, res.data)
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load key result: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    }
  }

  function resetForm() {
    form.value = {
      title: '',
      description: '',
      value_definition: '',
      unit: '',
      start_value: 0,
      current_value: 0,
      target_value: 0,
      status: '',
      priority: '',
      complexity: '',
      start_date: '',
      end_date: '',
      member_id: '',
      objective_id: '',
    }
  }

  async function onSave() {
    try {
      const payload = {
        ...form.value,
        member_id: form.value.member_id ? Number(form.value.member_id) : null,
        objective_id: form.value.objective_id
          ? Number(form.value.objective_id)
          : null,
      }
      if (isEdit.value) {
        await api.put(`/key-results/${props.keyResultId}`, payload)
      } else {
        await api.post('/key-results', payload)
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
