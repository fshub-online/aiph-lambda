<template>
  <v-card elevation="8">
    <v-card-title>
      System Users
    </v-card-title>
    <v-card-subtitle>
      Manage users in the system.
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
        Add User
      </v-btn>
      <v-text-field
        v-model="search"
        class="flex-grow-1 elevation-2"
        clearable
        density="compact"
        label="Search users"
        prepend-inner-icon="mdi-magnify"
        style="height: 40px;"
      />
    </div>
    <div class="d-flex">
      <v-data-table
        class="elevation-2 ml-4 mr-4 mt-4 mb-4"
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        loading-text="Loading users..."
        multi-sort
        :search="search"
        @update:sort-by="val => sortBy.value = val"
      >
        <template #item.actions="{ item }">
          <v-icon
            class="mr-2"
            color="primary"
            size="small"
            title="Edit user"
            @click="emit('edit', item)"
          >mdi-pencil</v-icon>
          <v-icon
            color="error"
            size="small"
            title="Delete user"
            @click="confirmDelete(item)"
          >mdi-delete</v-icon>
        </template>
      </v-data-table>
    </div>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete user <b>{{ userToDelete?.user_name }}</b>?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="deleteUser">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
  import { computed, defineEmits, onMounted, ref } from 'vue';
  import api from '@/api';

  const emit = defineEmits(['edit', 'delete', 'add']);

  const users = ref([]);
  const loading = ref(false);
  const search = ref('');
  const sortBy = ref([]);

  const deleteDialog = ref(false);
  const userToDelete = ref(null);
  const deleteLoading = ref(false);

  const snackbar = ref({ show: false, text: '', color: 'error' });

  const headers = [
    { title: 'User Name', value: 'user_name', sortable: true },
    { title: 'First Name', value: 'first_name', sortable: true },
    { title: 'Last Name', value: 'last_name', sortable: true },
    { title: 'e-mail', value: 'email', sortable: true },
    { title: 'Phone', value: 'phone', sortable: true },
    { title: 'Notes', value: 'notes', sortable: false },
    { title: 'Actions', value: 'actions', sortable: false },
  ];

  const filteredUsers = computed(() => {
    if (!search.value) return users.value;
    const s = search.value.toLowerCase();
    return users.value.filter(
      u =>
        u.user_name?.toLowerCase().includes(s) ||
        u.full_name?.toLowerCase().includes(s) ||
        u.email?.toLowerCase().includes(s) ||
        u.phone?.toLowerCase().includes(s) ||
        u.notes?.toLowerCase().includes(s)
    );
  });

  async function fetchUsers () {
    loading.value = true;
    try {
      const res = await api.get('/users');
      users.value = res.data;
    } catch (e) {
      snackbar.value = {
        show: true,
        text: 'Failed to load users: ' + (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      };
      users.value = [];
    } finally {
      loading.value = false;
    }
  }

  function confirmDelete (user) {
    userToDelete.value = user;
    deleteDialog.value = true;
  }

  async function deleteUser () {
    if (!userToDelete.value) return;
    deleteLoading.value = true;
    try {
      await api.delete(`/users/${userToDelete.value.id || userToDelete.value.user_name}`);
      deleteDialog.value = false;
      userToDelete.value = null;
      await fetchUsers();
    } catch (e) {
      snackbar.value = {
        show: true,
        text: 'Delete failed: ' + (e?.response?.data?.detail || e.message || String(e)),
        color: 'error',
      };
      deleteDialog.value = false;
      userToDelete.value = null;
    } finally {
      deleteLoading.value = false;
    }
  }

  onMounted(fetchUsers);

  // Expose fetchUsers for parent refresh
  defineExpose({ fetchUsers });
</script>
