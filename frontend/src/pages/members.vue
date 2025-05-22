<template>
  <v-container class="py-8">
    <h1>Team Members</h1>
    <MemberTable ref="memberTableRef" @add="onAddMember" @edit="onEditMember" />
    <MemberEditDialog
      :member-id="editMemberId"
      :open="editDialogOpen"
      @close="editDialogOpen = false"
      @saved="onMemberSaved"
    />
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import MemberTable from '@/components/member/MemberTable.vue'
  import MemberEditDialog from '@/components/member/MemberEditDialog.vue'

  const editDialogOpen = ref(false)
  const editMemberId = ref(null)
  const memberTableRef = ref(null)

  function onEditMember(member) {
    editMemberId.value = member.id
    editDialogOpen.value = true
  }

  function onAddMember() {
    editMemberId.value = null
    editDialogOpen.value = true
  }

  function onMemberSaved() {
    editDialogOpen.value = false
    memberTableRef.value?.fetchMembers?.()
  }
</script>
