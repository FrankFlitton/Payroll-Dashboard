<template>
  <div id="app">
    <a-layout>
      <a-layout-sider>Sider</a-layout-sider>

        <a-layout>
          <a-layout-header>Header</a-layout-header>

          <a-layout-content>
            <router-view></router-view>
          </a-layout-content>

          <a-layout-footer>Footer</a-layout-footer>
        </a-layout>
    </a-layout>
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
</style>
