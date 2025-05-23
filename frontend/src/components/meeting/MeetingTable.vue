<template>
  <v-card elevation="8">
    <v-card-title> Meetings </v-card-title>
    <v-card-subtitle> Manage meetings in the system. </v-card-subtitle>
    <v-divider class="ml-4 mr-4 mb-4 mt-4" thickness="2" />
    <div class="d-flex align-center ml-4 mr-4 mb-2" style="gap: 12px">
      <v-btn
        class="elevation-2"
        color="primary"
        prepend-icon="mdi-plus"
        style="height: 40px; min-width: 120px"
        @click="emit('add')"
      >
        Add Meeting
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search meetings"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredMeetings"
        :loading="loading"
        loading-text="Loading meetings..."
        multi-sort
        :search="search"
        :style="{ tableLayout: 'fixed' }"
        @update:sort-by="(val) => (sortBy.value = val)"
      >
        <template #item.lead_name="{ item }">
          <span>
            {{
              item.lead_member &&
              item.lead_member.first_name &&
              item.lead_member.last_name
                ? item.lead_member.first_name + ' ' + item.lead_member.last_name
                : item.lead_name || item.lead_member_id || ''
            }}
          </span>
        </template>
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit meeting"
            @click="emit('edit', item)"
            >mdi-pencil</v-icon
          >
          <v-icon
            color="error"
            size="small"
            title="Delete meeting"
            @click="confirmDelete(item)"
            >mdi-delete</v-icon
          >
        </template>
      </v-data-table>
    </div>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete meeting
          <b>{{ meetingToDelete?.title }}</b
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteMeeting"
            >Delete</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-card>
</template>

<script setup>
  import { computed, defineEmits, onMounted, ref } from 'vue'
  import api from '@/api'

  const emit = defineEmits(['edit', 'delete', 'add'])
  const meetings = ref([])
  const loading = ref(false)
  const search = ref('')
  const sortBy = ref([])

  const deleteDialog = ref(false)
  const meetingToDelete = ref(null)
  const deleteLoading = ref(false)
  const snackbar = ref({ show: false, text: '', color: 'error' })

  const headers = [
    { title: 'Title', value: 'title', sortable: true, width: '30%' },
    { title: 'Lead', value: 'lead_name', sortable: true, width: '25%' },
    { title: 'Date', value: 'date', sortable: true, width: '10%' },
    { title: 'Time', value: 'time', sortable: true, width: '10%' },
    {
      title: 'Duration (min)',
      value: 'duration',
      sortable: true,
      width: '15%',
    },
    { title: 'Actions', value: 'actions', sortable: false, width: '10%' },
  ]

  const filteredMeetings = computed(() => {
    if (!search.value) return meetings.value
    const s = search.value.toLowerCase()
    return meetings.value.filter(
      (m) =>
        m.title?.toLowerCase().includes(s) ||
        m.minutes?.toLowerCase().includes(s) ||
        String(m.date)?.toLowerCase().includes(s) ||
        String(m.time)?.toLowerCase().includes(s)
    )
  })

  const memberMap = ref({})

  async function fetchLeadMembers(meetings) {
    const ids = [
      ...new Set(meetings.map((m) => m.lead_member_id).filter(Boolean)),
    ]
    if (ids.length === 0) return {}
    try {
      const res = await api.get('/members')
      const map = {}
      for (const m of res.data) {
        map[m.id] = m
      }
      memberMap.value = map
    } catch {
      memberMap.value = {}
    }
  }

  async function fetchMeetings() {
    loading.value = true
    try {
      const res = await api.get('/meetings')
      await fetchLeadMembers(res.data)
      meetings.value = res.data.map((m) => ({
        ...m,
        lead_name: memberMap.value[m.lead_member_id]
          ? `${memberMap.value[m.lead_member_id].first_name} ${memberMap.value[m.lead_member_id].last_name}`
          : m.lead_member_id || '',
      }))
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load meetings: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      meetings.value = []
    } finally {
      loading.value = false
    }
  }

  function confirmDelete(meeting) {
    meetingToDelete.value = meeting
    deleteDialog.value = true
  }

  async function deleteMeeting() {
    if (!meetingToDelete.value) return
    deleteLoading.value = true
    try {
      await api.delete(`/meetings/${meetingToDelete.value.id}`)
      deleteDialog.value = false
      meetingToDelete.value = null
      await fetchMeetings()
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Delete failed: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      deleteDialog.value = false
      meetingToDelete.value = null
    } finally {
      deleteLoading.value = false
    }
  }

  onMounted(fetchMeetings)
  defineExpose({ fetchMeetings })
</script>

<style scoped>
  .v-data-table th:nth-child(1),
  .v-data-table td:nth-child(1) {
    width: 30%;
  }
  .v-data-table th:nth-child(2),
  .v-data-table td:nth-child(2) {
    width: 15%;
  }
  .v-data-table th:nth-child(3),
  .v-data-table td:nth-child(3) {
    width: 15%;
  }
  .v-data-table th:nth-child(4),
  .v-data-table td:nth-child(4) {
    width: 15%;
  }
  .v-data-table th:nth-child(5),
  .v-data-table td:nth-child(5) {
    width: 15%;
  }
  .v-data-table th:nth-child(6),
  .v-data-table td:nth-child(6) {
    width: 10%;
  }
</style>
