<template>
  <div id="app">
    <v-app>
      <!-- Global loading element -->
      <global-loading/>

      <!-- Navbar -->
      <v-app-bar app color='f_primary' class='navbar' max-height="56px" short scroll-off-screen dark flat clipped-left>

        <!-- Logo -->
        <v-img :src='websiteLogo' class='logo' contain max-height='40px' max-width='40px'/>
        <v-toolbar-title class='site-title'>
          <router-link :to="{ name: 'Home'}">
            <span class='emphasis'>Variant</span>
            <span>Hunter</span>
          </router-link>
        </v-toolbar-title>

        <v-spacer/>

        <v-btn v-if='$route.name!=="About"' class='hidden-xs-only mr-1 app-container f_primary--text' color="f_tertiary"
               elevation="0" rounded small>
          <router-link :to="{ name: 'About'}">
            About this tool
          </router-link>
        </v-btn>
      </v-app-bar>

      <!-- App body container -->
      <v-main :class="$route.name==='About'?'bg_var2':''">
        <router-view/>
      </v-main>
    </v-app>
  </div>
</template>

<script>

import GlobalLoading from "@/components/general/basic/GlobalLoading";

export default {
  name: 'App',
  components: {GlobalLoading},
  data() {
    return {
      /** VariantHunter logo */
      websiteLogo: require('./assets/logo.svg'),
    }
  }
}
</script>

<style>

/** Navbar overlapping visibility */
.navbar {
  z-index: 15 !important;
}

/* Site logo */
.logo {
  background-color: white;
  border-radius: 12px;
  margin-left: 17px;
}

/* Site title styles*/
.site-title {
  font-size: 33px;
  margin-left: 20px;
  text-transform: uppercase;
  letter-spacing: -2px;
  font-weight: 200;
}

.emphasis {
  letter-spacing: -1px;
  font-weight: 600;
  margin-right: 6px;
}

</style>
