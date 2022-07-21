<script>

export default {
  name: 'App',

  data() {
    return {
      ideas: [],
    }
  },

  async created() {
    let response = await fetch("http://localhost:8000/api/ideas/")
    console.log(await response.json())
  }
}
</script>

<template>
  <p>Hello</p>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
