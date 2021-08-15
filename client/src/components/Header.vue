<template>
  <header class="header">
    <h1 class="header__title">FileX</h1>
    <form class="header__search-wrapper">
      <input class="header__search-input" />
      <button class="header__search-btn">
        <img
          src="@/assets/icons/header/search.svg"
          class="header__search-icon"
          type="submit"
        />
      </button>
    </form>
    <div class="header__auth">
      <span class="header__user">@username</span>
      <button class="header__logout">Log out</button>
    </div>
  </header>
</template>
<style lang="scss" scoped>
.header {
  width: 100%;
  padding: 15px 25px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  background: colors.$f-black;
  color: colors.$f-lite;
  border-radius: 12px;
  &__title {
    margin: 0 20px 0 0;
  }
  &__search {
    &-wrapper {
      height: 40px;
      width: calc(100% - 330px);
      display: flex;
    }
    &-input {
      height: 100%;
      width: calc(100% - 45px);
      padding-left: 15px;
      box-sizing: border-box;
      font-size: 20px;
      background: colors.$f-white;
      border-radius: 20px 0 0 20px;
      border: none;
      outline: none;
    }
    &-btn {
      width: 45px;
      height: 100%;
      border-radius: 0 20px 20px 0;
      border: none;
      background: colors.$f-white;
    }
    &-icon {
      width: 24px;
      height: 24px;
    }
  }
  &__auth {
    margin-left: auto;
  }
  &__user {
    font-size: 18px;
    font-style: italic;
  }
  &__logout {
    margin-left: 10px;
    height: 30px;
    padding: 0 18px;
    background: colors.$f-lite;
    font-weight: 400;
    font-size: 18px;
    border: none;
    outline: none;
    border-radius: 10px;
  }
}
@media screen and (max-width: 767px) {
  .header {
    &__title {
      font-size: 24px;
    }
    &__search {
      &-wrapper {
        display: none;
      }
    }
  }
}
@media screen and (max-width: 359px) {
  .header {
    padding: 15px;
    &__title {
      font-size: 24px;
    }
  }
}
</style>
