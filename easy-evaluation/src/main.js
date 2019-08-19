import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import globalVariables from './global_variables'

Vue.prototype.global = globalVariables

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
