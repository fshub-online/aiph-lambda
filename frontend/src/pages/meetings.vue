<template>
  <v-container class="py-8">
    <MeetingTable
      ref="meetingTableRef"
      @add="onAddMeeting"
      @delete="onDeleteMeeting"
      @edit="onEditMeeting"
    />
    <MeetingEditDialog
      :meeting-id="editingMeetingId"
      :open="editDialogOpen"
      @close="closeEditDialog"
      @saved="onMeetingSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import MeetingTable from '@/components/meeting/MeetingTable.vue'
  import MeetingEditDialog from '@/components/meeting/MeetingEditDialog.vue'

  const meetingTableRef = ref(null)
  const editDialogOpen = ref(false)
  const editingMeetingId = ref(null)

  function onAddMeeting() {
    editingMeetingId.value = null
    editDialogOpen.value = true
  }
  function onEditMeeting(meeting) {
    editingMeetingId.value = meeting.id
    editDialogOpen.value = true
  }
  function closeEditDialog() {
    editDialogOpen.value = false
  }
  function onMeetingSaved() {
    editDialogOpen.value = false
    meetingTableRef.value?.fetchMeetings?.()
  }
  function onDeleteMeeting() {
    meetingTableRef.value?.fetchMeetings?.()
  }
</script>
