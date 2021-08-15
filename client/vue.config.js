module.exports = {
  css: {
    loaderOptions: {
      sass: {
        prependData: '@use "@/assets/scss/colors.scss";',
      },
    },
  },
};
