<template>
  <div id="app" class="d-flex flex-column">
    <b-navbar toggleable="md" type="dark" variant="primary" class="pt-3 pb-3">
      <b-container>
        <b-navbar-brand href="#">
          <img src="https://www.waveapps.com/assets/img/logo-full-black.svg" alt="WAVE">
        </b-navbar-brand>
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
  background: white !important;
}
footer {
  background: rgb(215, 217, 224)
}
</style>
