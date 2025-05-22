<template>
  <v-container class="py-8">
    <h1>Objectives</h1>
    <ObjectiveTable
      ref="objectiveTableRef"
      @add="onAddObjective"
      @edit="onEditObjective"
    />
    <ObjectiveEditDialog
      :objective-id="editObjectiveId"
      :open="editDialogOpen"
      @close="editDialogOpen = false"
      @saved="onObjectiveSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import ObjectiveTable from '@/components/objective/ObjectiveTable.vue'
  import ObjectiveEditDialog from '@/components/objective/ObjectiveEditDialog.vue'

  const editDialogOpen = ref(false)
  const editObjectiveId = ref(null)
  const objectiveTableRef = ref(null)

  function onEditObjective(objective) {
    editObjectiveId.value = objective.id
    editDialogOpen.value = true
  }

  function onAddObjective() {
    editObjectiveId.value = null
    editDialogOpen.value = true
  }

  function onObjectiveSaved() {
    editDialogOpen.value = false
    objectiveTableRef.value?.fetchObjectives?.()
  }
</script>
