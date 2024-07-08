<template>
  <div class="container">
    <div class="text-body2">Entrar em uma conta já existente:</div>
    <q-input standard v-model="username" label="Digite seu nome de usuário..."></q-input>
    <q-input standard v-model="password" label="Digite a sua senha..." type="password"></q-input>
    <q-btn color="secondary" label="Entrar" @click="handleLogin" class="q-mt-md q-mb-sm"></q-btn>
    <ConfirmedBanner v-show="authenticationResult && isAuthenticated" :message="authenticationResult" />
    <ErrorBanner v-show="authenticationResult && !isAuthenticated" :message="authenticationResult" />
    <br>
    <div class="text-body2">Não possui uma conta? <router-link to="/criarConta">Crie uma aqui!</router-link></div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import ErrorBanner from '../components/ErrorBanner.vue'
import ConfirmedBanner from '../components/ConfirmedBanner.vue'

export default {
  components: {
    ConfirmedBanner,
    ErrorBanner
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const isAuthenticated = computed(() => store.getters['user/getIsAuthenticated'])
    const authenticationResult = computed(() => store.getters['user/getAuthenticationResult'])

    const handleLogin = async () => {

      await store.dispatch('user/login', {
        username: username.value,
        password: password.value
      })
    }

    // Watcher to redirect on succesful login
    watch(isAuthenticated, (newValue) => {
      if (newValue) {
        router.push('/home')
      }
    })

    return {
      username,
      password,
      isAuthenticated,
      authenticationResult,
      handleLogin
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  background-color: white;
  padding: 10px;
  border: 2px solid black;
  border-radius: 5px;
  width: 80%;
  max-width: 400px;
  margin: 0 auto;
  margin-top: 50px;
}
</style>
