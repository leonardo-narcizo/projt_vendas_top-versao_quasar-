import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory, useRouter } from 'vue-router'
import routes from './routes'
import { useStore } from 'vuex'

const createHistory = process.env.SERVER
  ? createMemoryHistory
  : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

const Router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  routes,
  history: createHistory(process.env.VUE_ROUTER_BASE)
})

// Guarda de navegação para verificar autenticação
Router.beforeEach((to, from, next) => {
  const store = useStore()

  if (to.meta.requiresAuth && !store.getters['user/getIsAuthenticated']) {
    console.warn(`Acesso negado à rota ${to.fullPath}. Façã login para ter acesso à esta rota`)
    next('/')  // Redireciona para a página de login
  } else {
    next()  // Permite a navegação para a rota solicitada
  }
})

export default Router
