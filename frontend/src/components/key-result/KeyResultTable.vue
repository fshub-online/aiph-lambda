<template>
  <v-card elevation="8">
    <v-card-title> Key Results </v-card-title>
    <v-card-subtitle> Manage key results in the system. </v-card-subtitle>
    <v-divider class="ml-4 mr-4 mb-4 mt-4" thickness="2" />
    <div class="d-flex align-center ml-4 mr-4 mb-2" style="gap: 12px">
      <v-btn
        class="elevation-2"
        color="primary"
        prepend-icon="mdi-plus"
        style="height: 40px; min-width: 120px"
        @click="emit('add')"
      >
        Add Key Result
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search key results"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredKeyResults"
        :loading="loading"
        loading-text="Loading key results..."
        multi-sort
        :search="search"
        @update:sort-by="(val) => (sortBy.value = val)"
      >
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit key result"
            @click="emit('edit', item)"
            >mdi-pencil</v-icon
          >
          <v-icon
            color="error"
            size="small"
            title="Delete key result"
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
          Are you sure you want to delete key result
          <b>{{ keyResultToDelete?.title }}</b
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteKeyResult"
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
  const keyResults = ref([])
  const loading = ref(false)
  const search = ref('')
  const sortBy = ref([])

  const deleteDialog = ref(false)
  const keyResultToDelete = ref(null)
  const deleteLoading = ref(false)
  const snackbar = ref({ show: false, text: '', color: 'error' })

  const headers = [
    { title: 'Title', value: 'title', sortable: true },
    { title: 'Priority', value: 'priority', sortable: true },
    { title: 'Status', value: 'status', sortable: true },
    { title: 'Complexity', value: 'complexity', sortable: true },
    { title: 'Current Value', value: 'current_value', sortable: true },
    { title: 'Target Value', value: 'target_value', sortable: true },
    { title: 'Unit', value: 'unit', sortable: true },
    { title: 'Actions', value: 'actions', sortable: false },
  ]

  const filteredKeyResults = computed(() => {
    if (!search.value) return keyResults.value
    const s = search.value.toLowerCase()
    return keyResults.value.filter(
      (k) =>
        k.title?.toLowerCase().includes(s) ||
        k.description?.toLowerCase().includes(s) ||
        k.priority?.toLowerCase().includes(s) ||
        k.status?.toLowerCase().includes(s) ||
        k.complexity?.toLowerCase().includes(s)
    )
  })

  async function fetchKeyResults() {
    loading.value = true
    try {
      const res = await api.get('/key-results')
      keyResults.value = res.data
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Failed to load key results: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      keyResults.value = []
    } finally {
      loading.value = false
    }
  }

  function confirmDelete(keyResult) {
    keyResultToDelete.value = keyResult
    deleteDialog.value = true
  }

  async function deleteKeyResult() {
    if (!keyResultToDelete.value) return
    deleteLoading.value = true
    try {
      await api.delete(`/key-results/${keyResultToDelete.value.id}`)
      deleteDialog.value = false
      keyResultToDelete.value = null
      await fetchKeyResults()
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Delete failed: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
      deleteDialog.value = false
      keyResultToDelete.value = null
    } finally {
      deleteLoading.value = false
    }
  }

  onMounted(fetchKeyResults)
  defineExpose({ fetchKeyResults })
</script>
