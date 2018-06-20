<template>
  <div class="home">

    <b-container class="bv-input">
      <b-row><h2>Welcome to Chat</h2></b-row>
      <b-row>
        <b-form @submit="onSubmit">
          <b-form-input id="userName"
                        type="text"
                        v-model="user"
                        required
                        placeholder="Enter User Name">
          </b-form-input>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-form>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  data() {
    return {
      test: null,
      userName: 'sdsdsds',
      user: null
    }
  },
  name: 'home',
  components: {
    HelloWorld
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
