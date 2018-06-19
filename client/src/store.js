import Vue from "vue";
import Vuex from "vuex";
import {getRooms} from "./http-common";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    rooms: [],
    user_rooms: [],
    loading: [],
    user_name: null
  },
  mutations: {
    updateRooms(state, rooms) {
      state.rooms = rooms
    },
    updateUserRooms(state, rooms) {
      state.user_rooms = rooms
    },
    changeLoadingState(state, loading) {
      state.loading = loading
    },
    setUserName(state, userName) {
      state.user_name = userName
    }
  },
  actions: {
    getUserRooms({
      commit
    }, user_name ) {
      getRooms(user_name).then((response) => {
        // console.log(response.data, this)
        commit('updateUserRooms', response.data)
        commit('changeLoadingState', false)
      })
    },
    getAllRooms({
      commit
    }) {
      getRooms().then((response) => {
        // console.log(response.data, this)
        commit('updateRooms', response.data)
        commit('changeLoadingState', false)
      })
    },
}
});