<template>
  <v-app-bar app color="primary">
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title class="text-h6"
      >AI Performance Hub (<span style="font-family: serif">&lambda;</span
      >)</v-toolbar-title
    >
    <v-spacer />

    <!-- Login button when not authenticated -->
    <v-btn
      v-if="!authStore.isAuthenticated"
      icon
      title="Login"
      @click="showLoginDialog = true"
    >
      <v-icon>mdi-login</v-icon>
    </v-btn>

    <!-- User menu when authenticated -->
    <div v-else class="d-flex align-center mr-4">
      <span class="mr-2">
        {{ authStore.user.first_name }} {{ authStore.user.last_name }}
      </span>
      <UserMenu
        :user="authStore.user"
        @change-password="showPasswordDialog = true"
        @edit-profile="showProfileDialog = true"
        @logout="handleLogout"
      />
    </div>

    <!-- Theme toggle button -->
    <v-btn icon @click="$emit('toggle-theme')">
      <v-icon>{{
        isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent'
      }}</v-icon>
    </v-btn>

    <!-- Login dialog -->
    <LoginDialog v-model="showLoginDialog" />

    <!-- User profile dialog -->
    <UserProfileDialog
      v-if="authStore.user"
      v-model="showProfileDialog"
      :user="authStore.user"
    />

    <!-- Change password dialog -->
    <ChangePasswordDialog v-model="showPasswordDialog" />
  </v-app-bar>
</template>

<script setup>
  import { defineEmits, defineProps, onMounted, ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import LoginDialog from '@/components/user/LoginDialog.vue'
  import UserMenu from '@/components/user/UserMenu.vue'
  import UserProfileDialog from '@/components/user/UserProfileDialog.vue'
  import ChangePasswordDialog from '@/components/user/ChangePasswordDialog.vue'

  defineProps({
    isDark: Boolean,
  })

  defineEmits(['toggle-drawer', 'toggle-theme'])

  const authStore = useAuthStore()
  const showLoginDialog = ref(false)
  const showProfileDialog = ref(false)
  const showPasswordDialog = ref(false)

  function handleLogout() {
    authStore.logout()
  }

  onMounted(async () => {
    // Initialize auth state from stored token
    await authStore.initialize()
  })
</script>
