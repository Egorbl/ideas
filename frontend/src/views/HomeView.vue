<template>
  <div class="home">
    <IdeasList :categoryId="this.$route.params.category" />
  </div>
</template>

<script>
import IdeasList from "@/components/IdeasList.vue"

export default {
  name: 'HomeView',
  components: {
    IdeasList
  },
}
</script>
