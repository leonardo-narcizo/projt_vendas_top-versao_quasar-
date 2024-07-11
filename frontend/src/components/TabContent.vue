<template>
  <div  style="overflow-y: auto;">
    <div class="div-header text-h6 q-mb-lg q-px-xs">
      <div>
        {{ currentFilterLabel }}
      </div>
      <div class="filtros"> 
        <q-btn 
          dense flat round icon="filter_alt" 
          label="Filtros"
          color="secondary"
          @click="menu = true"
        />
        <filter-menu :onSelect="updateFilter" :currentTab="currentTab" />
      </div>
    </div>

    <q-table
      :rows="proposals"
      :columns="columns"
      row-key="id_proposta"
      :rows-per-page-options="[0]"
      flat
      bordered
      class="q-table-fixed"
    >
      <template v-slot:body-cell="props">
        <q-td :props="props" :key="props.key">
          <template v-if="props.col.name === 'comprador_username'">
            {{ props.row.comprador_username }}
          </template>
          <template v-if="props.col.name === 'proprietario_username'">
            {{ props.row.proprietario_username }}
          </template>
          <template v-else-if="props.col.name === 'data_proposta'">
            {{ props.row.data_proposta }}
          </template>
          <template v-else-if="props.col.name === 'car_props'">
            {{ props.row.marca }} / {{ props.row.modelo }}
          </template>
          <template v-else-if="props.col.name === 'actions'">
            <q-btn flat round icon="visibility" @click="viewProposal(props.row)" />
          </template>
        </q-td>
      </template>

      <!-- Slot para mensagem personalizada quando não há dados -->
      <template v-slot:no-data>
        <div class="q-table__simple text-center" style="padding: 20px;">
          <q-icon name="warning" size="50px" color="warning" />
          <div class="warning-label text-subtitle2">{{ proposalsSearchResult }}</div>
        </div>
      </template>
    </q-table>

    <status-on-footer
      :show-footer="showFooter"
      :status="footerStatus"
      :message="footerMessage"
      @update-show-footer="updateShowFooter"
    />

    <received-proposal-dialog
      v-if="currentTab == 'received'"
      :currentFilter="currentFilter"
      :proposal="selectedProposal"
      :dialogVisible="dialogVisible"
      @update:model-value="dialogVisible = $event"
      @accept="acceptProposal"
      @negotiate="negotiateProposal"
      @reject="rejectProposal"
    />

    <sent-proposal-dialog
      v-if="currentTab == 'sent'"
      :currentFilter="currentFilter"
      :proposal="selectedProposal"
      :dialogVisible="dialogVisible"
      @update:model-value="dialogVisible = $event"
      @edit="editProposal"
      @cancel="cancelProposal"
    />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useStore } from 'vuex';
import FilterMenu from './FilterMenu.vue';
import StatusOnFooter from './StatusOnFooter.vue';
import ReceivedProposalDialog from './dialogs/ReceivedProposalDialog.vue';
import SentProposalDialog from './dialogs/SentProposalDialog.vue';

export default {
  components: {
    FilterMenu,
    StatusOnFooter,
    ReceivedProposalDialog, // Registrar o componente importado
    SentProposalDialog
  },
  props: {
    currentTab: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const updateShowFooter = (value) => {
      showFooter.value = value;
    };

    const store = useStore();
    const username = sessionStorage.getItem('username');
    const showFooter = ref(false);
    const footerStatus = ref('');
    const footerMessage = ref('');

    const proposalsList = computed(() => store.getters['proposal/getProposalsList']);
    const proposalsSearchResult = computed(() => store.getters['proposal/getProposalsSearchResult']);

    const proposals = ref([]);

    const columns = ref([
      { name: 'comprador_username', label: 'Enviado por', align: 'left' },
      { name: 'data_proposta', label: 'Data', align: 'left' },
      { name: 'car_props', label: 'Fabricante/Modelo', align: 'right' },
      { name: 'actions', label: 'Ações', align: 'right' }
    ]);

    const currentFilterLabel = ref('Não lidas');
    const currentFilter = ref('nao_vista');

    if (props.currentTab == 'sent') {
      currentFilterLabel.value = 'Sem retorno'
      columns.value[0].name = 'proprietario_username'
      columns.value[0].label = 'Enviado para'
    }

    
  
    const dialogVisible = ref(false);
    const selectedProposal = ref(null);

    const viewProposal = (row) => {
      selectedProposal.value = row;
      dialogVisible.value = true;
      console.log('clicou p ver proposta: ', selectedProposal.value)
    };

    // Getters do vuex, que serão reutilizados dentro das ações das propostas
    const isConfirmedAction = computed(() => store.getters['proposal/getConfirmResult'])
    const actionMessage = computed(() => store.getters['proposal/getProposalMessageResult'])

    const editProposal = (row) => {
      console.log('Editar proposta', row);
    };
   
    // Function reutilizavel p fazer ações sobre as propostas
    const actionOnProposal = async (actionsCallName, object) => {

      try {
        await store.dispatch(actionsCallName, object)

        if (isConfirmedAction.value == true) {
          showFooter.value = true
          footerStatus.value = 'confirmed'
          footerMessage.value = actionMessage.value
        }
        else {
          showFooter.value = true
          footerStatus.value = 'error'
          footerMessage.value = actionMessage.value
        }
      }
      catch (err) {
        console.error('erro ao acionar a store: ', err)
        showFooter.value = true
        footerStatus.value = 'error'
        footerMessage.value = 'Erro durante a comunicação com o servidor'
      }
      finally {
        store.commit('proposal/clearCurrentProposal')
        console.log('currentProposal limpada')
      }

      dialogVisible.value = false;
    };


    const rejectProposal = () => actionOnProposal('proposal/rejectProposal', { id_proposta: selectedProposal.value.id_proposta });
    const cancelProposal = () => actionOnProposal('proposal/cancelProposal', { id_proposta: selectedProposal.value.id_proposta })
    const acceptProposal = () => {
      actionOnProposal('proposal/acceptProposal', {  id_proposta: selectedProposal.value.id_proposta, preco_proposto:selectedProposal.value.preco_proposto, id_carro: selectedProposal.value.id_carro, comprador_username: selectedProposal.value.comprador_username })

      store.dispatch('socket/listenSoldCar')
    }

    const negotiateProposal = async () => {
      console.log('Iniciar negociação:', selectedProposal.value);
      // Primeiramente mudar o estado da proposta de 'nao_visto' para 'em_negociacao'
      await actionOnProposal('proposal/negotiateProposal', { id_proposta: selectedProposal.value.id_proposta })

      // Após ja mudado o estado, mudar para a tab de chats
      setTimeout(() => {
        emit('update-current-tab', 'chats');

        // Após a aba ser trocada, criar um novo chat
        setTimeout(async () => {
          try {
            await store.dispatch('socket/criarNovoChat', {
              proprietarioUsername: selectedProposal.value.proprietario_username,
              compradorUsername: selectedProposal.value.comprador_username,
              idCarro: selectedProposal.value.id_carro
            });
          } catch (err) {
            console.error('Erro ao criar o chat de negociação!', err);
          }

          dialogVisible.value = false;
        }, 500); // Ajustar o tempo conforme necessário
      }, 1000); // Tempo de exibição do footer dinâmico
    }


    const handleSearchProposals = async (tab, filter) => {
      try {
        await store.dispatch('proposal/searchProposals', { tab, filter, username });
        console.log('filtro atual: ', currentFilter.value)

        proposals.value = proposalsList.value.map(proposal => ({
          id_carro: proposal.id_carro,
          comprador_username: proposal.comprador_username,
          proprietario_username: proposal.proprietario_username,
          id_proprietario: proposal.id_proprietario,
          id_antigo_dono: proposal.id_antigo_dono,
          data_proposta: proposal.data_proposta,
          marca: proposal.marca,
          modelo: proposal.modelo,
          descricao: proposal.descricao,
          preco_proposto: proposal.preco_proposto,
          conclusao: proposal.conclusao,
          id_proposta: proposal.id_proposta // Chave única p referênciar na q-table
        }));
      } catch (err) {
        console.error('Erro ao buscar propostas:', err);
        showFooter.value = true;
        footerStatus.value = 'error';
        footerMessage.value = 'Erro ao buscar propostas';
      }
    };

    const updateFilter = ({ filter, label }) => {
      currentFilter.value = filter;
      currentFilterLabel.value = label;
      handleSearchProposals(props.currentTab, filter);
    };

    watch(() => props.currentTab, (newTab) => {
      handleSearchProposals(newTab, currentFilter.value);
    });

    onMounted(() => {
      handleSearchProposals(props.currentTab, currentFilter.value);
    });



    return {
      proposalsList,
      proposalsSearchResult,
      username,
      showFooter,
      footerStatus,
      footerMessage,
      proposals,
      columns,
      currentFilter,
      currentFilterLabel,
      isConfirmedAction,
      actionMessage,
      actionOnProposal,
      viewProposal,
      editProposal,
      updateFilter,
      dialogVisible,
      selectedProposal,
      updateShowFooter,
      acceptProposal,
      negotiateProposal,
      rejectProposal,
      cancelProposal
    };
  }
};

</script>

<style lang="scss" scoped>
.div-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 2px solid black;
  border-radius: 5px;
}
.filtros {
  margin-left: auto;
}

.q-table-fixed {
  width: 100%;
}
.warning-label {
  display: inline;
  margin-left: 10px;
}
</style>
