<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">Change Password</v-card-title>
      <v-card-text>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="5000">
          {{ snackbarMessage }}
        </v-snackbar>
        <v-form ref="form" @submit.prevent="handleSubmit">
          <v-text-field
            v-model="currentPassword"
            autocomplete="current-password"
            :disabled="isLoading"
            label="Current Password"
            required
            type="password"
          />
          <v-text-field
            v-model="newPassword"
            autocomplete="new-password"
            :disabled="isLoading"
            label="New Password"
            required
            :rules="[v => !!v || 'Password is required', v => v.length >= 8 || 'Password must be at least 8 characters']"
            type="password"
          />
          <v-text-field
            v-model="confirmPassword"
            autocomplete="new-password"
            :disabled="isLoading"
            label="Confirm New Password"
            required
            :rules="[v => v === newPassword || 'Passwords do not match']"
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
          :disabled="isLoading || !canSubmit"
          :loading="isLoading"
          @click="handleSubmit"
        >
          Update Password
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue';
  import { useAuthStore } from '../stores/auth';

  const props = defineProps({
    modelValue: Boolean,
  });

  const emit = defineEmits(['update:modelValue']);

  // Local dialog visibility state synced with prop
  const dialogVisible = ref(props.modelValue);

  watch(() => props.modelValue, val => {
    dialogVisible.value = val;
  });

  watch(dialogVisible, val => {
    if (val !== props.modelValue) {
      emit('update:modelValue', val);
    }
    if (val) {
      error.value = '';
      success.value = '';
      snackbar.value = false;
      snackbarMessage.value = '';
      snackbarColor.value = 'error';
    }
  });

  // Setup store and form refs
  const authStore = useAuthStore();
  const form = ref(null);
  const currentPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');
  const error = ref('');
  const success = ref('');
  const isLoading = ref(false);
  const snackbar = ref(false);
  const snackbarMessage = ref('');
  const snackbarColor = ref('error');

  // Validate form fields
  const canSubmit = computed(() => {
    return currentPassword.value &&
      newPassword.value &&
      confirmPassword.value &&
      newPassword.value === confirmPassword.value &&
      newPassword.value.length >= 8;
  });

  async function handleSubmit () {
    if (!canSubmit.value) return;

    error.value = '';
    success.value = '';
    isLoading.value = true;
    snackbar.value = false;
    snackbarMessage.value = '';
    snackbarColor.value = 'error';

    try {
      await authStore.changePassword(currentPassword.value, newPassword.value);
      // Show success and reset form
      success.value = 'Password updated successfully.';
      snackbarMessage.value = success.value;
      snackbarColor.value = 'success';
      snackbar.value = true;
      currentPassword.value = '';
      newPassword.value = '';
      confirmPassword.value = '';
      setTimeout(() => {
        emit('update:modelValue', false);
      }, 1200);
    } catch (err) {
      error.value = `Failed to change password (error message: ${err.message}).`;
      snackbarMessage.value = error.value;
      snackbarColor.value = 'error';
      snackbar.value = true;
    } finally {
      isLoading.value = false;
    }
  }
</script>
