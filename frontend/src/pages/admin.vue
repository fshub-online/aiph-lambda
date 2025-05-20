<template>
  <v-container class="py-8">
    <h1>Administration</h1>
    <UserTable
      ref="userTableRef"
      class="mt-8"
      @add="onAddUser"
      @edit="onEditUser"
    />
    <UserEditDialog
      :open="editDialogOpen"
      :user-id="editUserId"
      @close="editDialogOpen = false"
      @saved="onUserSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue';
  import UserTable from '@/components/UserTable.vue';
  import UserEditDialog from '@/components/UserEditDialog.vue';

  const editDialogOpen = ref(false);
  const editUserId = ref(null);
  const userTableRef = ref(null);

  function onEditUser (user) {
    editUserId.value = user.id || user.user_name;
    editDialogOpen.value = true;
  }

  function onAddUser () {
    editUserId.value = null;
    editDialogOpen.value = true;
  }

  function onUserSaved () {
    editDialogOpen.value = false;
    userTableRef.value?.fetchUsers?.();
  }
</script>
