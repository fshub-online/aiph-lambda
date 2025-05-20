<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list>
      <v-list-item
        prepend-icon="mdi-home"
        router
        title="Home"
        to="/"
      />
      <!-- Add more navigation items here -->
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
  import { computed, defineEmits, defineProps } from 'vue'

  const props = defineProps({
    modelValue: Boolean,
  })
  const emit = defineEmits(['update:modelValue'])

  const drawer = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })
</script>
