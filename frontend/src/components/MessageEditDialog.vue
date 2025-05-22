<template>
  <v-dialog v-model="dialogOpen" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{ isEdit ? 'Edit Message' : 'Add Message' }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-text-field v-model="form.title" label="Title" required />
          <v-textarea v-model="form.message" label="Message" required />
          <v-select
            v-model="form.priority"
            :items="priorities"
            label="Priority"
            required
          />
          <v-text-field
            v-model="form.display_start"
            label="Display Start"
            type="date"
          />
          <v-text-field
            v-model="form.display_end"
            label="Display End"
            type="date"
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
    messageId: { type: [Number, String], default: null },
  })
  const emit = defineEmits(['close', 'saved'])

  const dialogOpen = ref(false)

  watch(() => props.open, val => {
    dialogOpen.value = val
  })

  watch(dialogOpen, val => {
    if (!val) emit('close')
  })

  const form = ref({
    title: '',
    message: '',
    priority: '',
    display_start: '',
    display_end: '',
  })
  const priorities = ref([])
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.messageId)

  watch(() => props.open, async val => {
    if (val) {
      await fetchPriorities()
      if (props.messageId) {
        await loadMessage()
      } else {
        resetForm()
      }
    }
  })

  async function fetchPriorities () {
    try {
      const res = await api.get('/message-priorities')
      priorities.value = res.data
    } catch (e) {
      snackbar.value = { show: true, text: e?.response?.data?.detail || e.message || String(e) || 'Failed to load priorities', color: 'error' }
    }
  }

  async function loadMessage () {
    try {
      const res = await api.get(`/messages/${props.messageId}`)
      Object.assign(form.value, res.data)
    } catch (e) {
      snackbar.value = { show: true, text: e?.response?.data?.detail || e.message || String(e) || 'Failed to load message', color: 'error' }
    }
  }

  function resetForm () {
    form.value = { title: '', message: '', priority: '', display_start: '', display_end: '' }
  }

  async function onSave () {
    try {
      if (isEdit.value) {
        await api.put(`/messages/${props.messageId}`, form.value)
      } else {
        await api.post('/messages', form.value)
      }
      emit('saved')
      emit('close')
    } catch (e) {
      snackbar.value = { show: true, text: e?.response?.data?.detail || e.message || String(e) || 'Save failed', color: 'error' }
    }
  }
</script>
