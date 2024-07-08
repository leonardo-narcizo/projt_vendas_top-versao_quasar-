<template>
    <div class="q-pa-xl">
      <q-card>
        <q-tabs
          v-model="tab"
          dense
          class="black bg-secondary"
          active-color="black"
          indicator-color="black"
          active-bg-color="primary"
          align="justify"
        >
          <q-tab name="received" label="Recebidas" />
          <q-tab name="sent" label="Enviadas" />
          <q-tab name="chats" label="Chats de Negociação" />
        </q-tabs>
  
        <q-separator />
   
        <q-tab-panels v-model="tab" animated>

            <q-tab-panel name="received">
                <TabContent :currentTab="tab" @update-current-tab="updateCurrentTab"/>
            </q-tab-panel>
            
            <q-tab-panel name="sent">
                <TabContent :currentTab="tab"/>
            </q-tab-panel>
              
            <q-tab-panel name="chats">
                <chat-list />
            </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </template>
  
  <script>

  import { ref } from 'vue'
  import TabContent from '../components/TabContent.vue'
  import ChatList from '../components/ChatList.vue'
  
  export default {
    components: {
        TabContent,
        ChatList
    },
    setup () {
      const tab = ref('received')

      const updateCurrentTab = (value) => {
      tab.value = value;
    };

      return {
        tab,
        updateCurrentTab
      }
    }
  }
  </script>
  
  <style lang="scss" scoped>
  .q-card {
    max-width: 1100px; /* Definindo a largura máxima do q-card */
    margin: 0 auto; /* Centralizando o q-card */
  }
  </style>
  