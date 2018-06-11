import Vue from "vue";
import Vuex from "vuex";
import {getBlogs} from './http_common';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    blogs:[],
    loading:[]
  },
  mutations: {
    updateBlogs(state, blogs) {
      state.blogs = blogs
    },
    changeLoadingState(state, loading) {
      state.loading = loading
    }
  },
  actions: {
    getAllBlogs({
      commit
    }) {
      getBlogs().then((response) => {
        console.log(response.data, this)
        commit('updateBlogs', response.data)
        commit('changeLoadingState', false)
      })
    },
  getBlogById({
    commit
  }, id) {
    console.log(id)
    getBlogs(id.Id).then((response) => {
      console.log(response.data, this)
      commit('updateBlogs', response.data)
    })
  },
}
});