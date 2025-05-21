<template>
  <v-card elevation="8">
    <v-card-title>
      Members
    </v-card-title>
    <v-card-subtitle>
      Manage members in the system.
    </v-card-subtitle>
    <v-divider class="ml-4 mr-4 mb-4 mt-4" thickness="2" />
    <div class="d-flex align-center ml-4 mr-4 mb-2" style="gap: 12px;">
      <v-btn
        class="elevation-2"
        color="primary"
        prepend-icon="mdi-account-plus"
        style="height: 40px; min-width: 120px;"
        @click="emit('add')"
      >
        Add Member
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search members"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px;"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredMembers"
        :loading="loading"
        loading-text="Loading members..."
        multi-sort
        :search="search"
        @update:sort-by="val => sortBy.value = val"
      >
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit member"
            @click="emit('edit', item)"
          >mdi-pencil</v-icon>
          <v-icon
            color="error"
            size="small"
            title="Delete member"
            @click="confirmDelete(item)"
          >mdi-delete</v-icon>
        </template>
      </v-data-table>
    </div>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete member <b>{{ memberToDelete?.first_name }} {{ memberToDelete?.last_name }}</b>?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteMember">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-card>
</template>

<script setup>
  import { computed, defineEmits, onMounted, ref } from 'vue';
  import api from '@/api';

  const emit = defineEmits(['edit', 'delete', 'add']);

  const members = ref([]);
  const loading = ref(false);
  const search = ref('');
  const sortBy = ref([]);

  const deleteDialog = ref(false);
  const memberToDelete = ref(null);
  const deleteLoading = ref(false);
  const snackbar = ref({ show: false, text: '', color: 'error' });

  const headers = [
    { title: 'First Name', value: 'first_name', sortable: true },
    { title: 'Last Name', value: 'last_name', sortable: true },
    { title: 'Position', value: 'position', sortable: true },
    { title: 'Email', value: 'email', sortable: true },
    { title: 'Phone', value: 'phone', sortable: true },
    { title: 'Actions', value: 'actions', sortable: false },
  ];

  const filteredMembers = computed(() => {
    if (!search.value) return members.value;
    const s = search.value.toLowerCase();
    return members.value.filter(
      m =>
        m.first_name?.toLowerCase().includes(s) ||
        m.last_name?.toLowerCase().includes(s) ||
        m.position?.toLowerCase().includes(s) ||
        m.email?.toLowerCase().includes(s) ||
        m.phone?.toLowerCase().includes(s) ||
        m.note?.toLowerCase().includes(s)
    );
  });

  async function fetchMembers () {
    loading.value = true;
    try {
      const res = await api.get('/members');
      members.value = res.data;
    } catch (e) {
      snackbar.value = {
        show: true,
        text: 'Failed to load members: ' + (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      };
      members.value = [];
    } finally {
      loading.value = false;
    }
  }

  function confirmDelete (member) {
    memberToDelete.value = member;
    deleteDialog.value = true;
  }

  async function deleteMember () {
    if (!memberToDelete.value) return;
    deleteLoading.value = true;
    try {
      await api.delete(`/members/${memberToDelete.value.id}`);
      deleteDialog.value = false;
      memberToDelete.value = null;
      await fetchMembers();
    } catch (e) {
      snackbar.value = {
        show: true,
        text: 'Delete failed: ' + (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      };
      deleteDialog.value = false;
      memberToDelete.value = null;
    } finally {
      deleteLoading.value = false;
    }
  }

  onMounted(fetchMembers);

  defineExpose({ fetchMembers });
</script>
