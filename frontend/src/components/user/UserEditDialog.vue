<template>
  <v-dialog v-model="internalOpen" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        <span class="text-h6">{{ isEdit ? 'Edit User' : 'Add User' }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" @submit.prevent="saveUser">
          <v-text-field v-model="formData.user_name" :disabled="isEdit" label="Username" required />
          <v-text-field v-model="formData.first_name" label="First Name" />
          <v-text-field v-model="formData.last_name" label="Last Name" />
          <v-text-field v-model="formData.email" label="Email" required type="email" />
          <v-text-field v-model="formData.phone" label="Phone" />
          <v-textarea v-model="formData.notes" label="Notes" rows="2" />
          <v-text-field
            v-if="!isEdit"
            v-model="formData.password"
            label="Password"
            required
            type="password"
          />
        </v-form>
        <v-alert v-if="error" class="mt-2" type="error">{{ error }}</v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="loading" text @click="closeDialog">Cancel</v-btn>
        <v-btn color="primary" :disabled="loading" :loading="loading" @click="saveUser">
          {{ isEdit ? 'Save' : 'Create' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue';
  import api from '@/api';

  const props = defineProps({
    userId: { type: [String, Number], default: null },
    open: { type: Boolean, default: false },
  });
  const emit = defineEmits(['close', 'saved']);

  const internalOpen = ref(false);
  const loading = ref(false);
  const error = ref('');
  const form = ref(null);

  const isEdit = computed(() => !!props.userId);
  const formData = ref({
    user_name: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    notes: '',
    password: '', // Only for new user
  });

  watch(() => props.open, val => {
    internalOpen.value = val;
    if (val) {
      loadUser();
    }
  });

  watch(() => internalOpen.value, val => {
    if (!val) emit('close');
  });

  async function loadUser () {
    error.value = '';
    if (isEdit.value) {
      loading.value = true;
      try {
        const res = await api.get(`/users/${props.userId}`);
        Object.assign(formData.value, res.data);
      } catch (e) {
        error.value = e?.response?.data?.detail || 'Failed to load user.';
      } finally {
        loading.value = false;
      }
    } else {
      // Reset for new user
      Object.assign(formData.value, {
        user_name: '', first_name: '', last_name: '', email: '', phone: '', notes: '', password: '',
      });
    }
  }

  async function saveUser () {
    error.value = '';
    loading.value = true;
    try {
      let res;
      if (isEdit.value) {
        const data = { ...formData.value };
        delete data.password;
        res = await api.put(`/users/${props.userId}`, data);
      } else {
        res = await api.post('/users', formData.value);
      }
      emit('saved', res.data);
      internalOpen.value = false;
    } catch (e) {
      error.value = e?.response?.data?.detail || 'Failed to save user.';
    } finally {
      loading.value = false;
    }
  }

  function closeDialog () {
    internalOpen.value = false;
  }
</script>
