<template>
  <div id="app">
    <div id="nav">
      <b-button variant="success" to="/">Home</b-button>
      <b-button variant="success" to="/about">Chat </b-button>
      <hr>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
}
</script>

