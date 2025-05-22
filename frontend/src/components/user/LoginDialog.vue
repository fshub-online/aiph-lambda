<template>
  <v-dialog max-width="400px" :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title class="text-h5">Login</v-card-title>
      <v-card-text>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="5000">
          {{ snackbarMessage }}
        </v-snackbar>
        <v-form ref="form" @submit.prevent="handleLogin">
          <v-text-field
            v-model="username"
            autocomplete="username"
            :disabled="isLoading"
            label="Username"
            required
          />
          <v-text-field
            v-model="password"
            autocomplete="current-password"
            :disabled="isLoading"
            label="Password"
            required
            type="password"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          :disabled="isLoading"
          text
          @click="$emit('update:modelValue', false)"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          :disabled="isLoading"
          :loading="isLoading"
          @click="handleLogin"
        >
          Login
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { ref, watch } from 'vue';
  import { useAuthStore } from '@/stores/auth';

  const props = defineProps({
    modelValue: Boolean,
  });

  const emit = defineEmits(['update:modelValue']);

  const authStore = useAuthStore();
  const form = ref(null);
  const username = ref('');
  const password = ref('');
  const error = ref('');
  const success = ref('');
  const isLoading = ref(false);
  const snackbar = ref(false);
  const snackbarMessage = ref('');
  const snackbarColor = ref('error');

  // Reset error/snackbar when dialog opens
  watch(() => props.modelValue, val => {
    if (val) {
      error.value = '';
      snackbar.value = false;
      snackbarMessage.value = '';
      snackbarColor.value = 'error';
    }
  });

  async function handleLogin () {
    error.value = '';
    isLoading.value = true;
    snackbar.value = false;
    snackbarMessage.value = '';
    snackbarColor.value = 'error';
    try {
      await authStore.login({
        username: username.value,
        password: password.value,
      });
      // Reset form after successful login
      success.value = 'Login successful.';
      snackbarMessage.value = success.value;
      snackbarColor.value = 'success';
      snackbar.value = true;
      username.value = '';
      password.value = '';
      setTimeout(() => {
        emit('update:modelValue', false);
      }, 1200);
    } catch (err) {
      error.value = `Login failed. Please check your credentials (error returned: ${err.message}).`;
      snackbarMessage.value = error.value;
      snackbarColor.value = 'error';
      snackbar.value = true;
    } finally {
      isLoading.value = false;
    }
  }
</script>
