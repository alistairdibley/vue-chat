<template>
  <div id="app">
    <div id="nav">
      <b-button variant="success" to="/">Home</b-button>
      <b-button variant="success" to="/messages">Messages </b-button>
      <hr>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
}
</script>

