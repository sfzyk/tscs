<template>

  <div id="app" :style='note1'>
    <div id="nav">
      <NavMenu />
    </div>
    <router-view />
  </div>
</template>

<script>
import NavMenu from "@/components/NavMenu.vue";
export default {
  components: {
    NavMenu
  },
  data() {
    return {
      note1: {
        backgroundSize: "cover",
        backgroundImage: "url(" + require("@/assets/p3.jpg") + ")",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
        height: "100%",
        position: "fixed",
        overflow: "auto",
        width: "100%"
      }
    };
  }
};
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  width: 100%;
}
#nav {
  padding: 5px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
