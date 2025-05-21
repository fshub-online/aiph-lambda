/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  // Allow access to index (home) for everyone
  if (to.path === '/' || to.name === 'index') {
    return next()
  }
  // If not authenticated, redirect to index and show warning
  if (!auth.isAuthenticated) {
    // Show warning after navigation
    next({ path: '/', query: { authRequired: '1' } })
    return
  }
  // Otherwise, allow navigation
  next()
})

// Show warning snackbar on index if redirected due to auth
router.afterEach(to => {
  if (to.path === '/' && to.query.authRequired === '1') {
    // Use a global event or store to trigger snackbar
    setTimeout(() => {
      const event = new CustomEvent('show-auth-warning')
      window.dispatchEvent(event)
    }, 100)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
