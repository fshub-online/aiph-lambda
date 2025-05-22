<template>
  <v-card elevation="8">
    <v-card-title> Objectives </v-card-title>
    <v-card-subtitle> Manage objectives in the system. </v-card-subtitle>
    <v-divider class="ml-4 mr-4 mb-4 mt-4" thickness="2" />
    <div class="d-flex align-center ml-4 mr-4 mb-2" style="gap: 12px">
      <v-btn
        class="elevation-2"
        color="primary"
        prepend-icon="mdi-plus"
        style="height: 40px; min-width: 120px"
        @click="emit('add')"
      >
        Add Objective
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search objectives"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredObjectives"
        :loading="loading"
        loading-text="Loading objectives..."
        multi-sort
        :search="search"
        :style="{ tableLayout: 'fixed' }"
        @update:sort-by="(val) => (sortBy.value = val)"
      >
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit objective"
            @click="emit('edit', item)"
            >mdi-pencil</v-icon
          >
          <v-icon
            color="error"
            size="small"
            title="Delete objective"
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
          Are you sure you want to delete objective
          <b>{{ objectiveToDelete?.title }}</b
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteObjective"
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
  const objectives = ref([])
  const loading = ref(false)
  const search = ref('')
  const sortBy = ref([])

  const deleteDialog = ref(false)
  const objectiveToDelete = ref(null)
  const deleteLoading = ref(false)
  const snackbar = ref({ show: false, text: '', color: 'error' })

  const headers = [
    { title: 'Title', value: 'title', sortable: true, width: '30%' },
    { title: 'Priority', value: 'priority', sortable: true, width: '15%' },
    { title: 'Status', value: 'status', sortable: true, width: '15%' },
    { title: 'Start Date', value: 'start_date', sortable: true, width: '15%' },
    { title: 'End Date', value: 'end_date', sortable: true, width: '15%' },
    { title: 'Actions', value: 'actions', sortable: false, width: '10%' },
  ]

  const filteredObjectives = computed(() => {
    if (!search.value) return objectives.value
    const s = search.value.toLowerCase()
    return objectives.value.filter(
      (o) =>
        o.title?.toLowerCase().includes(s) ||
        o.description?.toLowerCase().includes(s) ||
        o.priority?.toLowerCase().includes(s) ||
        o.status?.toLowerCase().includes(s)
    )
  })

  async function fetchObjectives() {
    loading.value = true
    try {
      const res = await api.get('/objectives')
      objectives.value = res.data
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load objectives: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      objectives.value = []
    } finally {
      loading.value = false
    }
  }

  function confirmDelete(objective) {
    objectiveToDelete.value = objective
    deleteDialog.value = true
  }

  async function deleteObjective() {
    if (!objectiveToDelete.value) return
    deleteLoading.value = true
    try {
      await api.delete(`/objectives/${objectiveToDelete.value.id}`)
      deleteDialog.value = false
      objectiveToDelete.value = null
      await fetchObjectives()
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Delete failed: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      deleteDialog.value = false
      objectiveToDelete.value = null
    } finally {
      deleteLoading.value = false
    }
  }

  onMounted(fetchObjectives)
  defineExpose({ fetchObjectives })
</script>

<style scoped>
  .v-data-table th:nth-child(1),
  .v-data-table td:nth-child(1) {
    width: 30%;
  }
  .v-data-table th:nth-child(2),
  .v-data-table td:nth-child(2) {
    width: 20%;
  }
  .v-data-table th:nth-child(3),
  .v-data-table td:nth-child(3) {
    width: 20%;
  }
  .v-data-table th:nth-child(4),
  .v-data-table td:nth-child(4) {
    width: 20%;
  }
  .v-data-table th:nth-child(5),
  .v-data-table td:nth-child(5) {
    width: 10%;
  }
</style>
