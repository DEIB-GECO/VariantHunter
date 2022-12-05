<template>
  <div id="app">
    <v-app>
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

/* Styling for the website body todo: remove */
.main-body {
  height: calc(100vh - 57px);
  width: 100%;
  overflow-y: auto;
  float: left;
  position: relative;
}
</style>

<style>
/* Global variables for color palette and border radius */
:root {
  --primary-color: var(--v-primary-base);
  --secondary-color: var(--v-secondary-base);
  --tertiary-color-light: var(--v-tertiary-base);
  --tertiary-color-dark: var(--v-accent-base);
  --border-radius: 4px;
}


/* Body background color */
html, body {
  background: var(--v-f_primary-base);
}

#app {
  background: var(--v-bg_var1-base); /* to ensure readable downloadable images */
}

/* Border radius for the graph plots*/
.main-svg {
  border-radius: 4px;
}

.regular-plot .main-svg {
  border-radius: 4px 0 4px 4px;
}

/* Capitalize select items */
.v-select-list {
  text-transform: capitalize !important;
}


/* Plotly container */
.plotly-container {
  border-radius: var(--border-radius);
  width: 100%;
  background: white;
}

/* Prevent text-underline for links */
a, .site-title a {
  color: inherit !important;
  text-decoration: none !important;
}
</style>
