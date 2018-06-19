<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <b-button variant="success" to="/about">Disabled </b-button>
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
    <b-form @submit="onSubmit">
      <b-form-input id="userName"
                    type="text"
                    v-model="user"
                    required
                    placeholder="Enter User Name">
      </b-form-input>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form> 
  </div>
</template>

<script>
export default {
  data() {
    return {
      test: null,
      userName: 'sdsdsds',
      user: null
    }
  },
  methods: {
    onSubmit: function() {
      this.$store.commit('setUserName', this.user)
      this.$store.dispatch('getUserRooms', this.user)
      this.$router.push('/about')
    }
  }
}
</script>

