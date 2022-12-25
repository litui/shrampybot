<template>
  <router-view />
</template>

<style lang="scss">
  @import 'scss/main.scss';

  #app {
    font-family: 'Source Sans Pro', Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
  }

  body {
    margin: 0;
  }

  div.va-card {
    &__title {
      align-items: top;
      margin-left: 1em;
      font-family: 'Revalia';
      font-size: 10pt;
    }
  }

  h1 {
    font-size: 24pt;
  }
  h2 {
    font-size: 20pt;
  }
  h3 {
    font-size: 16pt;
  }
  h4 {
    font-size: 14pt;
  }
  h5 {
    font-size: 11pt;
  }

  h1,
  h2,
  h3,
  h4,
  h5 {
    font-family: 'Revalia';
    text-transform: uppercase;
  }

  a {
    span.logo {
      font-family: 'Revalia';
      font-size: 20pt;
      color: #ffbb22;
      #dot_text {
        font-family: 'Revalia';
        font-size: 20pt;
        color: #e42222;
      }
      #bot_text {
        font-family: 'Revalia';
        font-size: 20pt;
        color: #ffffff;
      }
    }
  }
  a {
    color: #ffbb22;
  }
</style>
