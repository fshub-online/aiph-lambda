<template>
  <v-dialog
    max-width="600px"
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card>
      <v-card-title class="text-h5">User Profile</v-card-title>
      <v-card-text>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="5000">
          {{ snackbarMessage }}
        </v-snackbar>
        <v-form ref="form" @submit.prevent="handleSubmit">
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userData.first_name"
                :disabled="isLoading"
                label="First Name"
                required
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userData.last_name"
                :disabled="isLoading"
                label="Last Name"
                required
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userData.email"
                :disabled="isLoading"
                label="Email"
                required
                type="email"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userData.phone"
                :disabled="isLoading"
                label="Phone"
                type="tel"
              />
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="userData.notes"
                auto-grow
                :disabled="isLoading"
                label="Notes"
                rows="3"
              />
            </v-col>
          </v-row>
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
          @click="handleSubmit"
        >
          Save Changes
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useAuthStore } from '@/stores/auth'

  const props = defineProps({
    modelValue: Boolean,
    user: Object,
  })

  const emit = defineEmits(['update:modelValue'])

  // Setup store and form refs
  const authStore = useAuthStore()
  const form = ref(null)
  const userData = ref({
    first_name: '',
    last_name: '',
    email: '',
    notes: '',
    phone: '',
  })
  const error = ref('')
  const success = ref('')
  const isLoading = ref(false)
  const snackbar = ref(false)
  const snackbarMessage = ref('')
  const snackbarColor = ref('error')

  // Watch for user changes to populate form
  watch(
    () => props.user,
    (newUser) => {
      if (newUser) {
        userData.value = {
          first_name: newUser.first_name || '',
          last_name: newUser.last_name || '',
          email: newUser.email || '',
          notes: newUser.notes || '',
          phone: newUser.phone || '',
        }
      }
    },
    { immediate: true }
  )

  async function handleSubmit() {
    error.value = ''
    success.value = ''
    isLoading.value = true
    snackbar.value = false
    snackbarMessage.value = ''
    snackbarColor.value = 'error'

    try {
      await authStore.updateProfile(userData.value)
      // Update user in store (already done in store)
      success.value = 'Profile updated successfully.'
      snackbarMessage.value = success.value
      snackbarColor.value = 'success'
      snackbar.value = true
      setTimeout(() => {
        emit('update:modelValue', false)
      }, 1200)
    } catch (err) {
      error.value = `Failed to update profile (error message: ${err.message}).`
      snackbarMessage.value = error.value
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      isLoading.value = false
    }
  }
</script>
