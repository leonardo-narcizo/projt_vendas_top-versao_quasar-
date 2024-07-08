<template>
    <div class="container">
      <div claas="text-body2">Criar uma nova conta:</div>
      <q-input standard v-model="username" label="Digite um novo nome de usuário..."></q-input>
      <q-input standard v-model="password" label="Digite uma nova senha..." type="password"></q-input>
      <q-option-group
        v-model="accountType"
        :options="accountTypeOptions"
        inline
        color="secondary"
        label="Tipo de Conta"
      ></q-option-group>
      <q-input
        v-if="accountType === 'Pessoa Jurídica'"
        standard
        v-model="cnpj"
        type="number"
        label="Digite o CNPJ..."
      ></q-input>
      <ErrorBanner v-if="showErrorBanner" :message="errorMessage" />
      <q-btn color="secondary" label="Criar Conta" @click="handleSignup" class="q-mt-md q-mb-md"></q-btn>
      <ConfirmedBanner v-if="showConfirmedBanner" :message="confirmedMessage" />
      <br>
      <div class="text-body2">Já possui uma conta? <router-link to="/">Faça login aqui!</router-link></div>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import ConfirmedBanner from '../components/ConfirmedBanner.vue'
  import ErrorBanner from '../components/ErrorBanner.vue'
  
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
      const accountType = ref('Pessoa Física')
      const cnpj = ref('')
      const isCreated = computed(() => store.getters['user/getIsCreated'])
      const signupResult = computed(() => store.getters['user/getSignupResult'])
      const showConfirmedBanner = ref(false)
      const confirmedMessage = ref('')
      const showErrorBanner = ref(false)
      const errorMessage = ref('')
  
      const accountTypeOptions = [
        { label: 'Pessoa Física', value: 'Pessoa Física' },
        { label: 'Pessoa Jurídica', value: 'Pessoa Jurídica' }
      ]
  
      const handleSignup = async () => {
        if (accountType.value === 'Pessoa Jurídica' && cnpj.value.length !== 14) {
          showErrorBanner.value = true
          errorMessage.value = 'CNPJ deve ter 14 dígitos'
          return
        }

        // Validando campos vazios
        if (username.value == '' || password.value == '') {
          showErrorBanner.value = true
          errorMessage.value = 'Preencha os campos corretamente!'
          return
        }
  
        await store.dispatch('user/signup', {
          username: username.value,
          password: password.value,
          cnpj: accountType.value === 'Pessoa Jurídica' ? cnpj.value : null
        });
  
        if (isCreated.value) {
          showConfirmedBanner.value = true
          confirmedMessage.value = signupResult.value

          // Retirando erros anteiores
          showErrorBanner.value = false
  
          setTimeout(() => {
            router.push('/')
          }, 1000)
        } else {
          showErrorBanner.value = true
          errorMessage.value = signupResult.value
        }
      }
  
      // Assiste ao valor de signupResult para mudanças
      watch(signupResult, (newVal) => {
        if (!isCreated.value) {
          showErrorBanner.value = true
          errorMessage.value = newVal
        }
      });
  
      return {
        username,
        password,
        accountType,
        cnpj,
        signupResult,
        isCreated,
        accountTypeOptions,
        handleSignup,
        showConfirmedBanner,
        confirmedMessage,
        showErrorBanner,
        errorMessage
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
  
  .q-radio {
    margin-bottom: 20px;
  }
  </style>
  