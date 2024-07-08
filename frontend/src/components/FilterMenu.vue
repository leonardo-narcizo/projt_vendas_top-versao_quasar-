<template>
    <q-menu v-model="menu" anchor="bottom right" self="top right">
      <q-list>
        <q-item v-if="currentTab == 'received'" clickable v-close-popup @click="selectFilter('nao_vista', 'Não lidas')">
          <q-item-section>Não lidas</q-item-section>
        </q-item>
        <q-item v-if="currentTab == 'sent'" clickable v-close-popup @click="selectFilter('nao_vista', 'Sem retorno')">
          <q-item-section>Sem retorno</q-item-section>
        </q-item>
        <q-item v-if="currentTab == 'received' || currentTab == 'sent'" clickable v-close-popup @click="selectFilter('em_negociacao', 'Em negociação')">
          <q-item-section>Em negociação</q-item-section>
        </q-item>
        <q-item v-if="currentTab == 'received' || currentTab == 'sent'" clickable v-close-popup @click="selectFilter('encerrada', 'Encerradas')">
          <q-item-section>Encerradas</q-item-section>
        </q-item>

        <!--Itens para a tab de chat-->
        <q-item v-if="currentTab == 'chats'" clickable v-close-popup @click="selectFilter('chat_venda', 'Chats de venda')">
          <q-item-section>Chats de venda</q-item-section>
        </q-item>
        <q-item v-if="currentTab == 'chats'" clickable v-close-popup @click="selectFilter('chat_compra', 'Chats de compra')">
          <q-item-section>Chats de compra</q-item-section>
        </q-item>

      </q-list>
    </q-menu>
  </template>
  
  <script>
  export default {
    props: {
      onSelect: {
        type: Function,
        required: true
      },
      currentTab: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        menu: false
      }
    },
    methods: {
      selectFilter(filter, label) {
        this.onSelect({ filter, label })
      }
    }
  }
  </script>
  
  <style scoped>
  /* Adicione estilo aqui, se necessário */
  </style>
  