<template>
  <div id="app" class="d-flex flex-column">
    <b-navbar toggleable="md" type="dark" variant="primary" class="pt-4 pb-4">
      <b-container>
        <b-navbar-brand href="#">Payroll App</b-navbar-brand>
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

<style lang="scss">
@import 'static/variables.scss';

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: rgb(241, 239, 239);
}
body, #app {
   min-height:100vh;
}
.flex-fill {
   flex:1 1 auto;
}
nav.bg-primary {
  background: linear-gradient(45deg, $c-primary, darken($c-primary, 13%));
}
footer {
  background: rgb(215, 217, 224)
}
</style>
