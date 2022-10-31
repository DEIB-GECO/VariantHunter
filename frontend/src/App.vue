<template>
   <div id="app">
     <v-app>
      <!-- Navbar -->
      <v-app-bar app :color='primary_color' class='navbar' max-height="56px" short scroll-off-screen  dark flat clipped-left>

        <!-- Logo -->
        <v-img :src='websiteLogo' class='logo' contain max-height='40px' max-width='40px' />
        <v-toolbar-title class='site-title'>
          <router-link to='/variant_hunter/'>
            <span class='emphasis'>Variant</span>
            <span>Hunter</span>
          </router-link>
        </v-toolbar-title>

        <v-spacer/>

        <v-btn v-if='$route.name!=="About"' class='hidden-xs-only mr-1 app-container primary--text' color="tertiary" elevation="0" rounded small>
          <router-link :to="{ name: 'About'}">
            About this tool
          </router-link>
        </v-btn>
      </v-app-bar>

      <v-main :class="$route.name==='About'?'white':''">
        <router-view />
      </v-main>
     </v-app>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'App',

  data () {
    return {
      /** VariantHunter logo */
      websiteLogo: require('./assets/logo.png'),

      /** Flag to show the new search shortcut */
      showSearchShortcut: false
    }
  },
  computed: {
    ...mapState(['primary_color'])
  },
  methods: {
    /** Scroll event handler to hide/show the search shortcut */
    scrollHandler (e) {
      this.showSearchShortcut = e.target.scrollTop > 440
    }
  }
}
</script>

<style>

/** Navbar overlapping visibility */
.navbar{
  z-index: 15 !important;
}

/* Site logo */
.logo{
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
  --primary-color: #014878;
  --secondary-color: #35b1ecff;
  --tertiary-color-light: #d2ecf8ff;
  --tertiary-color-dark: #1976d2ff;
  --border-radius: 4px;
}

/* Body background color */
body {
  background: var(--primary-color);
}
#app {
  background: var(--primary-color); /* to ensure readable downloadable images */
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
a, .site-title a{
    color: inherit !important;
    text-decoration: none !important;
}
</style>
