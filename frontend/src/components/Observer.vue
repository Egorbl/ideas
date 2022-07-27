<script>
export default {
    name: "app-observer",

    emits: ['intersect'],

    data() {
        return {
            observer: null,
        }
    },

    mounted() {
        this.observer = new IntersectionObserver(([entry]) => {
            if (entry && entry.isIntersecting) {
                console.log(entry)
                this.$emit('intersect');
            }
        })
        this.observer.observe(this.$el);
    }
}
</script>

<template>
    <div class="observer"></div>
</template>