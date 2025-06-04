import api from '@/api'
import { onMounted, ref } from 'vue'
import OrgTree from '@/components/member/OrgTree.vue'

const user = ref(null)
const member = ref(null)
const topManager = ref(null)
const orgTree = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    // 1. Get current user
    const userRes = await api.get('/oauth/me')
    user.value = userRes.data
    // 2. Get member for user
    const memberRes = await api.get(`/members/by-user/${user.value.id}`)
    member.value = memberRes.data
    // 3. Get top manager for member
    const topManagerRes = await api.get(
      `/members/${member.value.id}/top-manager`
    )
    topManager.value = topManagerRes.data
    // 4. Get org tree for top manager
    const orgTreeRes = await api.get(`/members/${topManager.value.id}/org-tree`)
    orgTree.value = orgTreeRes.data
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || String(e)
  } finally {
    loading.value = false
  }
})

export default {
  components: { OrgTree },
  setup() {
    return { user, member, topManager, orgTree, loading, error }
  },
}
