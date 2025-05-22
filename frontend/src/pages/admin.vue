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
    <MessageTable
      ref="messageTableRef"
      class="mt-8"
      @add="onAddMessage"
      @edit="onEditMessage"
    />
    <MessageEditDialog
      :message-id="editMessageId"
      :open="editMessageDialogOpen"
      @close="editMessageDialogOpen = false"
      @saved="onMessageSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue';
  import UserTable from '@/components/user/UserTable.vue';
  import UserEditDialog from '@/components/user/UserEditDialog.vue';
  import MessageTable from '@/components/message/MessageTable.vue';
  import MessageEditDialog from '@/components/message/MessageEditDialog.vue';


  const editDialogOpen = ref(false);
  const editUserId = ref(null);
  const userTableRef = ref(null);

  const editMessageDialogOpen = ref(false);
  const editMessageId = ref(null);
  const messageTableRef = ref(null);

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

  function onEditMessage (message) {
    editMessageId.value = message.id;
    editMessageDialogOpen.value = true;
  }

  function onAddMessage () {
    editMessageId.value = null;
    editMessageDialogOpen.value = true;
  }

  function onMessageSaved () {
    editMessageDialogOpen.value = false;
    messageTableRef.value?.fetchMessages?.();
  }
</script>
