<template>
  <div class="home">
    <button type="button" class="btn btn-primary" @click="addIdea">Add new idea</button>
    <IdeasList />
  </div>
</template>

<script>
import IdeasList from "@/components/IdeasList.vue"

export default {
  name: 'HomeView',
  components: {
    IdeasList
  },

  methods: {
    addIdea() {
      if (this.isUserAuthenticated()) {
        this.$router.push("ideaForm");
        return
      }
      this.$router.push("login");
    },
    isUserAuthenticated() {
      const accessToken = localStorage.getItem("accessToken");
      console.log("checking authentication");
      if (accessToken == null) {
        console.log("not authenticated");
        return false;
      }
      console.log("authenticated");
      return true;
    }
  }
}
</script>
