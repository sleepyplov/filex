<template>
  <div class="wrapper">
    <div class="wrapper__inner">
      <router-view />
    </div>
  </div>
</template>

<style lang="scss">
body {
  margin: 0;
}
.wrapper {
  width: 100%;
  height: 100vh;
  background: colors.$f-grey;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  &__inner {
    width: 100%;
    height: 100%;
    max-width: 1280px;
    // background: $f-dark;
    margin: 0 auto;
    padding-top: 7px;
    box-sizing: border-box;
  }
}
@media screen and (max-width: 1279px) {
  .wrapper {
    padding: 7px;
    box-sizing: border-box;
  }
}
</style>
