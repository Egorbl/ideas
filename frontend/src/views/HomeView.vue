<template>
  <div class="home">
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
}
</script>
