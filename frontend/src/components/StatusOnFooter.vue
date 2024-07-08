<template>
  <q-footer
    class="status-footer q-mb-md text-center q-flex-center"
    v-show="internalShowFooter"
    appear
    enter-active-class="animate-fadeIn"
    leave-active-class="animate-fadeOut"
  >
    <confirmed-banner v-if="status === 'confirmed'" :message="message" />
    <error-banner v-if="status === 'error'" :message="message" />
  </q-footer>
</template>

<script>
import { ref, watchEffect } from 'vue';
import ConfirmedBanner from "./ConfirmedBanner.vue";
import ErrorBanner from "./ErrorBanner.vue";

export default {
  components: {
    ConfirmedBanner,
    ErrorBanner
  },
  props: {
    showFooter: {
      type: Boolean,
      default: false
    },
    status: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const internalShowFooter = ref(false);

    // Monitora a prop showFooter usando watchEffect
    watchEffect(() => {
      if (props.showFooter) {
        internalShowFooter.value = true;
        setTimeout(() => {
          internalShowFooter.value = false;
          // Emite o evento para atualizar showFooter no pai(MAIS UM MERDA DE CONCEITO Q DEMOREI 1 DIA INTEIRO P ENTENDER OQ FAIZ! 'EMIT')
          // Emit:
          emit('update-show-footer', false);
        }, 1000);
      }
    });

    return {
      internalShowFooter
    };
  }
};
</script>

<style lang="scss" scoped>
.status-footer {
  width: 60%;
  margin: auto;
  margin-bottom: 15px; /* Adiciona uma margem inferior */
}

.animate-fadeIn-enter-active, .animate-fadeOut-leave-active {
  transition: opacity 0.5s;
}

.animate-fadeIn-enter, .animate-fadeOut-leave-to {
  opacity: 0;
}
</style>
