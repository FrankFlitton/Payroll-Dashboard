<template>
  <div id="app" class="d-flex flex-column">
    <b-navbar toggleable="md" type="dark" variant="primary">
      <b-container>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand href="#">PAYROLLTRON</b-navbar-brand>
      </b-container>
    </b-navbar>

    <b-container class="flex-fill">
      <router-view></router-view>
    </b-container>

    <footer class="p-3">
      Coded by Frank Flitton, 2018
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
body, #app {
   min-height:100vh;
}
.flex-fill {
   flex:1 1 auto;
}
footer {
  background: rgb(215, 217, 224)
}
</style>
