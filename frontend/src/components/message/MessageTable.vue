<template>
  <v-card class="elevation-8">
    <v-card-title> Messages </v-card-title>
    <v-card-subtitle>
      Manage system messages displayed on the home page.
    </v-card-subtitle>
    <v-divider class="ml-4 mr-4 mb-4 mt-4" thickness="2" />
    <div class="d-flex align-center ml-4 mr-4 mb-2" style="gap: 12px">
      <v-btn
        class="elevation-2"
        color="primary"
        prepend-icon="mdi-message-plus"
        style="height: 40px; min-width: 120px"
        @click="emit('add')"
      >
        Add Message
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search messages"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredMessages"
        :loading="loading"
        loading-text="Loading messages..."
        multi-sort
        :search="search"
        @update:sort-by="(val) => (sortBy.value = val)"
      >
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit message"
            @click="onEdit(item)"
            >mdi-pencil</v-icon
          >
          <v-icon
            color="error"
            size="small"
            title="Delete message"
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
          Are you sure you want to delete message
          <b>{{ messageToDelete?.title || messageToDelete?.id }}</b
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteMessage"
            >Delete</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
  import { computed, defineEmits, onMounted, ref } from 'vue'
  import api from '@/api'

  const emit = defineEmits(['add', 'edit'])
  const messages = ref([])
  const loading = ref(false)
  const search = ref('')
  const sortBy = ref([])
  const deleteLoading = ref(false)
  const snackbar = ref({ show: false, text: '', color: 'error' })

  const headers = [
    { title: 'Title', value: 'title', sortable: true },
    { title: 'Priority', value: 'priority', sortable: true },
    { title: 'Display Start', value: 'display_start', sortable: true },
    { title: 'Display End', value: 'display_end', sortable: true },
    { title: 'Actions', value: 'actions', sortable: false },
  ]

  const filteredMessages = computed(() => {
    if (!search.value) return messages.value
    const s = search.value.toLowerCase()
    return messages.value.filter(
      (m) =>
        (m.title && m.title.toLowerCase().includes(s)) ||
        (m.message && m.message.toLowerCase().includes(s)) ||
        (m.priority && m.priority.toLowerCase().includes(s))
    )
  })

  function fetchMessages() {
    loading.value = true
    api
      .get('/messages')
      .then((res) => {
        messages.value = res.data
      })
      .catch((e) => {
        snackbar.value = {
          show: true,
          text:
            'Failed to load messages: ' +
            (e?.response?.data?.detail || e.message || String(e)),
          color: 'error',
        }
      })
      .finally(() => {
        loading.value = false
      })
  }

  function onEdit(message) {
    emit('edit', message)
  }

  const deleteDialog = ref(false)
  const messageToDelete = ref(null)

  function confirmDelete(item) {
    messageToDelete.value = item
    deleteDialog.value = true
  }

  async function deleteMessage() {
    if (!messageToDelete.value) return
    deleteLoading.value = true
    try {
      await api.delete(`/messages/${messageToDelete.value.id}`)
      fetchMessages()
    } catch (e) {
      snackbar.value = {
        show: true,
        text:
          'Delete failed: ' +
          (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      }
    } finally {
      deleteLoading.value = false
      deleteDialog.value = false
      messageToDelete.value = null
    }
  }

  onMounted(fetchMessages)

  defineExpose({ fetchMessages })
</script>
