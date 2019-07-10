import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
      isLog:false,
      isWho:'1',
  },
  mutations: {
    setOnline() {
      this.state.isLog = true;
    }, setOffline() {
      this.state.isLog = false;
    },isStu(){
      this.state.isWho = '1'
    },isExp(){
      this.state.isWho = '2'
    },isAdm(){
      this.state.isWho = '3'
    }
  },
  actions: {

  }
})
