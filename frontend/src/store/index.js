import { store } from 'quasar/wrappers'
import { createStore } from 'vuex'

import user from './user-module'
import car from './car-module'
import proposal from './proposal-module'
import chat from './chat-module'

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store(function (/* { ssrContext } */) {
  const Store = createStore({
    modules: {
      user,
      car,
      proposal,
      chat
    },

    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: process.env.DEBUGGING
  })

  return Store
})
