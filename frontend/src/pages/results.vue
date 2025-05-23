<template>
  <v-container class="py-8">
    <KeyResultTable
      ref="keyResultTableRef"
      @add="onAddKeyResult"
      @edit="onEditKeyResult"
    />
    <KeyResultEditDialog
      :key-result-id="editKeyResultId"
      :open="editDialogOpen"
      @close="editDialogOpen = false"
      @saved="onKeyResultSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import KeyResultTable from '@/components/key-result/KeyResultTable.vue'
  import KeyResultEditDialog from '@/components/key-result/KeyResultEditDialog.vue'

  const editDialogOpen = ref(false)
  const editKeyResultId = ref(null)
  const keyResultTableRef = ref(null)

  function onEditKeyResult(keyResult) {
    editKeyResultId.value = keyResult.id
    editDialogOpen.value = true
  }

  function onAddKeyResult() {
    editKeyResultId.value = null
    editDialogOpen.value = true
  }

  function onKeyResultSaved() {
    editDialogOpen.value = false
    keyResultTableRef.value?.fetchKeyResults?.()
  }
</script>
