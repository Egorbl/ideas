<template>
  <div class="main-app">
    <Header :num="num" />
    <router-view @changeHeader="changeNum" />
  </div>
</template>

<script>
import Header from "./components/Header.vue"

export default {
  components: {
    Header,
  },
  data() {
    return {
      num: 12
    }
  },
  methods: {
    changeNum() {
      this.num += 1;
    }
  }
}
</script>

<!-- <style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style> -->

<style>
.main-app {
  word-wrap: break-word;
}

.my-card {
  border: 1px solid rgba(100, 100, 100, 0.7);
  background-color: rgba(218, 196, 196, 0.2)
}
</style>