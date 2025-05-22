<template>
  <v-app>
    <v-layout>
      <!-- Header -->
      <AppHeader
        :is-dark="isDark"
        @toggle-drawer="toggleDrawer"
        @toggle-theme="toggleTheme"
      />

      <!-- Sidebar -->
      <SideBar v-model="drawer" />

      <!-- Main content -->
      <v-main>
        <router-view />
      </v-main>

      <!-- Footer -->
      <AppFooter />
    </v-layout>
  </v-app>
</template>

<script setup>
  import { ref } from 'vue'
  import { useTheme } from 'vuetify'
  import AppFooter from '../components/AppFooter.vue'
  import AppHeader from '../components/AppHeader.vue'
  import SideBar from '../components/SideBar.vue'

  const drawer = ref(true) // Start with drawer open
  const theme = useTheme()
  const isDark = ref(false) // Start in light mode

  // Ensure theme is set to light on app start
  theme.global.name.value = 'light'

  function toggleDrawer() {
    drawer.value = !drawer.value
  }

  function toggleTheme() {
    theme.global.name.value = isDark.value ? 'light' : 'dark'
    isDark.value = !isDark.value
  }
</script>
