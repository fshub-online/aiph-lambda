<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list>
      <v-list-item prepend-icon="mdi-home" router title="Home" to="/" />

      <v-divider class="my-2" />

      <v-list-item
        prepend-icon="mdi-monitor-dashboard"
        router
        title="Dashboard"
        to="/dashboard"
      />
      <v-list-item
        prepend-icon="mdi-account-group"
        router
        title="Team Members"
        to="/members"
      />
      <v-list-item
        prepend-icon="mdi-bullseye-arrow"
        router
        title="Objectives"
        to="/objectives"
      />
      <v-list-item
        prepend-icon="mdi-account-hard-hat"
        router
        title="Key Results"
        to="/results"
      />
      <v-list-item
        prepend-icon="mdi-notebook"
        router
        title="Meetings"
        to="/meetings"
      />
      <v-list-item
        prepend-icon="mdi-certificate"
        router
        title="Evaluations"
        to="/evaluations"
      />

      <v-divider class="my-2" />
      <v-list-item
        prepend-icon="mdi-shield-crown"
        router
        title="Administration"
        to="/admin"
      />
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
    set: (val) => emit('update:modelValue', val),
  })
</script>
