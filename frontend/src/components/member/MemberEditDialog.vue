<template>
  <v-dialog v-model="dialogOpen" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{ isEdit ? 'Edit Member' : 'Add Member' }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-text-field v-model="form.first_name" label="First Name" required />
          <v-text-field v-model="form.last_name" label="Last Name" required />
          <v-text-field v-model="form.position" label="Position" required />
          <v-text-field v-model="form.email" label="Email" />
          <v-text-field v-model="form.phone" label="Phone" />
          <v-textarea v-model="form.note" label="Note" />
          <v-select
            v-model="form.supervisor_id"
            clearable
            :disabled="loadingSupervisors"
            item-title="label"
            item-value="id"
            :items="supervisorOptions"
            label="Supervisor"
            :loading="loadingSupervisors"
            return-object="false"
          />
          <v-select
            v-model="form.user_id"
            clearable
            :disabled="loadingUsers"
            item-title="label"
            item-value="id"
            :items="userOptions"
            label="User"
            :loading="loadingUsers"
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
    memberId: { type: [Number, String], default: null },
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
    first_name: '',
    last_name: '',
    position: '',
    email: '',
    phone: '',
    note: '',
    supervisor_id: '',
    user_id: '',
  })
  const snackbar = ref({ show: false, text: '', color: 'error' })
  const isEdit = computed(() => !!props.memberId)

  const supervisorOptions = ref([])
  const userOptions = ref([])
  const loadingSupervisors = ref(false)
  const loadingUsers = ref(false)

  watch(
    () => props.open,
    async (val) => {
      if (val) {
        loadingSupervisors.value = true
        loadingUsers.value = true
        try {
          // Load supervisors (members)
          const res = await api.get('/members')
          supervisorOptions.value = res.data.items
            ? res.data.items.map((m) => ({
                id: m.id,
                label: `${m.first_name} ${m.last_name}`,
              }))
            : res.data.map((m) => ({
                id: m.id,
                label: `${m.first_name} ${m.last_name}`,
              }))
        } catch {
          supervisorOptions.value = []
        } finally {
          loadingSupervisors.value = false
        }
        try {
          // Load users
          const res = await api.get('/users')
          userOptions.value = res.data.items
            ? res.data.items.map((u) => ({
                id: u.id,
                label: `${u.first_name || ''} ${u.last_name || ''} (${
                  u.username || u.email || u.id
                })`.trim(),
              }))
            : res.data.map((u) => ({
                id: u.id,
                label: `${u.first_name || ''} ${u.last_name || ''} (${
                  u.username || u.email || u.id
                })`.trim(),
              }))
        } catch {
          userOptions.value = []
        } finally {
          loadingUsers.value = false
        }
        if (props.memberId) {
          await loadMember()
        } else {
          resetForm()
        }
      }
    }
  )

  async function loadMember() {
    try {
      const res = await api.get(`/members/${props.memberId}`)
      Object.assign(form.value, res.data)
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load member: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    }
  }

  function resetForm() {
    form.value = {
      first_name: '',
      last_name: '',
      position: '',
      email: '',
      phone: '',
      note: '',
      supervisor_id: '',
      user_id: '',
    }
  }

  async function onSave() {
    try {
      // Patch: ensure supervisor_id and user_id are always numbers or null
      let supervisor_id = form.value.supervisor_id
      let user_id = form.value.user_id
      if (typeof supervisor_id === 'object' && supervisor_id !== null)
        supervisor_id = supervisor_id.id
      if (typeof user_id === 'object' && user_id !== null) user_id = user_id.id
      supervisor_id = supervisor_id ? Number(supervisor_id) : null
      user_id = user_id ? Number(user_id) : null
      const payload = {
        ...form.value,
        supervisor_id,
        user_id,
      }
      if (isEdit.value) {
        await api.put(`/members/${props.memberId}`, payload)
      } else {
        await api.post('/members', payload)
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
