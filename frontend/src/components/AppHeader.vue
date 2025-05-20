<template>
  <v-app-bar app color="primary">
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title class="text-h6">AI Performance Hub (<span style="font-family: serif">&lambda;</span>)</v-toolbar-title>
    <v-spacer />
    <v-btn icon @click="$emit('toggle-theme')">
      <v-icon>{{ isDark ? "mdi-white-balance-sunny" : "mdi-moon-waning-crescent" }}</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
  import { defineEmits, defineProps } from 'vue'
  const { isDark } = defineProps({
    isDark: Boolean,
  })
  defineEmits(['toggle-drawer', 'toggle-theme'])
</script>
