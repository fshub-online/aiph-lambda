<template>
  <router-view />
</template>

<script setup>
  console.log('meta:', import.meta)
  console.log('meta.env:', import.meta.env)
  console.log('meta.env.MODE:', import.meta.env.MODE)
  console.log('meta.env.VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)
</script>
