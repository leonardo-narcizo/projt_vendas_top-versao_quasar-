import LoginPage from 'src/pages/LoginPage.vue'
import CreateAcountPage from 'src/pages/CreateAcountPage.vue'
import ForgotPasswordPage from 'src/pages/ForgotPasswordPage.vue'
import HomePage from 'src/pages/HomePage.vue'
import PostCarPage from 'src/pages/PostCarPage.vue'
import BuyCarPage from 'src/pages/BuyCarPage.vue'
import ProposalsPage from 'src/pages/ProposalsPage.vue'
import Insights from 'src/pages/Insights.vue'
import ErrorNotFound from 'src/pages/ErrorNotFound.vue'

const routes = [
  {
    path: '/',
    component: () => import('layouts/StandardLayout.vue'),
    children: [
      { path: '', component: LoginPage },
      { path: '/criarConta', component: CreateAcountPage },
      { path: '/forgotPassword', component: ForgotPasswordPage }
    ]
  },
  {
    path: '/home',
    meta: { requiresAuth: true },
    component: () => import('layouts/HomeLayout.vue'),
    props: { namePage: 'Home' },
    children: [
      { path: '', component: HomePage }
    ]
  },
  {
    path: '/postCar',
    meta: { requiresAuth: true },
    component: () => import('layouts/HomeLayout.vue'),
    props: { namePage: 'Cadastro de Novo Carro' },
    children: [
      { path: '', component: PostCarPage }
    ]
  },
  {
    path: '/buyCar',
    meta: { requiresAuth: true },
    component: () => import('layouts/HomeLayout.vue'),
    props: { namePage: 'Compra de Carros' },
    children: [
      { path: '', component: BuyCarPage }
    ]
  },
  {
    path: '/proposals',
    meta: { requiresAuth: true },
    component: () => import('layouts/HomeLayout.vue'),
    props: { namePage: 'Propostas de Compra' },
    children: [
      { path: '', component: ProposalsPage }
    ]
  },
  {
    path: '/insights',
    meta: { requiresAuth: true },
    component: () => import('layouts/HomeLayout.vue'),
    props: { namePage: 'Insights' },
    children: [
      { path: '', component: Insights }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: ErrorNotFound
  }
]

export default routes
