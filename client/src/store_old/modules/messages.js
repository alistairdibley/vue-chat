import {getRooms} from "../../http-common";


const state =  {
      rooms: [],
      user_rooms: [],
      loading: [],
      user_name: null
    }

const mutations = {
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
    }

const actions =  {
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

  export default {
      namespaced: false,
      state,
      mutations,
      actions
  }