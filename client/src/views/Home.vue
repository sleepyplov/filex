<template>
  <Header />
  <h1 class="title">FileX is up n running!</h1>
</template>
<script>
import Header from '@/components/Header.vue';
export default {
  name: 'Home',
  components: { Header },
};
</script>
<style lang="scss" scoped>
.title {
  color: green;
}
</style>
