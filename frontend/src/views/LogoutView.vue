<script>

export default {
    created() {
        const accessToken = localStorage.getItem("accessToken");
        if (accessToken) {
            localStorage.removeItem("accessToken");
            location.reload();
        }
    }
}
</script>

<template>
    <p>You have been logged out</p>
</template>