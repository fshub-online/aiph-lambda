<template>
  <v-menu min-width="200px" rounded>
    <template #activator="{ props }">
      <v-btn icon v-bind="props">
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-text class="pa-4">
        <div class="text-h6">{{ user.first_name }} {{ user.last_name }}</div>
        <div class="text-subtitle-1 text-medium-emphasis">
          @{{ user.user_name }}
        </div>
      </v-card-text>
      <v-divider />
      <v-list>
        <v-list-item
          prepend-icon="mdi-account-edit"
          title="Edit Profile"
          @click="onEditProfile"
        />
        <v-list-item
          prepend-icon="mdi-key"
          title="Change Password"
          @click="onChangePassword"
        />
        <v-divider />
        <v-list-item
          prepend-icon="mdi-logout"
          title="Logout"
          @click="onLogout"
        />
      </v-list>
    </v-card>
  </v-menu>
</template>

<script setup>
  import { defineEmits, defineProps } from 'vue'

  defineProps({
    user: Object,
  })

  const emit = defineEmits(['logout', 'edit-profile', 'change-password'])

  function onLogout() {
    emit('logout')
  }

  function onEditProfile() {
    emit('edit-profile')
  }

  function onChangePassword() {
    emit('change-password')
  }
</script>
