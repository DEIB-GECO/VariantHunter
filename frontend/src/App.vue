<template>
  <v-app>

    <!-- Navbar -->
    <v-toolbar :color="primary_color" class="navbar" short dark flat>

      <!-- Logo -->
      <v-img :src="websiteLogo" contain max-height="39px" max-width="39px"/>
      <v-toolbar-title class="site-title">
        <span class="emphasis">Variant</span>
        <span>Hunter</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Scroll to top button -->
      <v-btn v-if="showSearchShortcut" class="hidden-xs-only" small outlined href="#top">
        <v-icon left>mdi-plus</v-icon>
        New analysis
      </v-btn>


      <!-- Navbar links to the other tools -->
      <!--      <v-toolbar-items class="hidden-lg-and-down navbar-links">-->
      <!--        <v-btn text href="https://github.com/DEIB-GECO/VariantHunter/wiki" target="_blank" class="navbar-link">-->
      <!--            <span>Wiki</span>-->
      <!--        </v-btn>-->

      <!--        <v-btn text href="/viruclust_gisaid/repo_static/about__variantHunter.html" target="_blank" class="navbar-link">-->
      <!--            <span>ABOUT</span>-->
      <!--        </v-btn>-->
      <!--      </v-toolbar-items>-->


      <!-- Menu links to the other tools -->
      <!--      <div class="hidden-xl-only">-->
      <!--        <v-menu>-->

      <!--          &lt;!&ndash; Menu icon &ndash;&gt;-->
      <!--          <template v-slot:activator="{ on, attrs }">-->
      <!--            <v-app-bar-nav-icon v-bind="attrs" v-on="on"/>-->
      <!--          </template>-->

      <!--          &lt;!&ndash; Menu links&ndash;&gt;-->
      <!--          <div class="nav-menu">-->
      <!--            <v-list-item class="menu-links">-->
      <!--              <v-list-item-content>-->
      <!--                      <v-list-item class="menu-links">-->
      <!--                          <v-list-item-content>-->
      <!--                            <v-btn text  href="https://github.com/DEIB-GECO/VariantHunter/wiki" target="_blank" class="menu-link">-->
      <!--                                <span>Wiki</span>-->
      <!--                            </v-btn>-->
      <!--                          </v-list-item-content>-->
      <!--                      </v-list-item>-->

      <!--                      <v-list-item class="menu-links">-->
      <!--                          <v-list-item-content>-->
      <!--                            <v-btn text  href="/viruclust_gisaid/repo_static/about__variantHunter.html" target="_blank" class="menu-link">-->
      <!--                                <span>ABOUT</span>-->
      <!--                            </v-btn>-->
      <!--                          </v-list-item-content>-->
      <!--                      </v-list-item>-->
      <!--          </div>-->
      <!--        </v-menu>-->
      <!--      </div>-->
    </v-toolbar>

    <v-main class="main-body" @scroll.native="scrollHandler">
      <TabView></TabView>
    </v-main>

  </v-app>
</template>

<script>

import {mapState} from "vuex";
import TabView from "@/components/TabsView";

export default {
  components: {
    TabView
  },

  data() {
    return {
      /** VariantHunter logo */
      websiteLogo: require('./assets/virusurf_logo.png'),

      /** Flag to show the new search shortcut */
      showSearchShortcut: false,
    }
  },
  computed: {
    ...mapState(['primary_color']),
  },
  methods: {

    /** Scroll event handler to hide/show the search shortcut */
    scrollHandler(e) {
      this.showSearchShortcut = e.target.scrollTop > 440
    }
  }
};

</script>

<style scoped>

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

/* Navbar links styling */
.navbar-links, .navbar-links > * {
  background: transparent;
}

.navbar-link {
  width: 100px !important;
}

.navbar-link-large {
  width: 200px !important;
}

.navbar-link-large img, .menu-link-large img {
  vertical-align: middle;
  justify-content: left;
  margin: 4px 0 2px 8px;
}

/* Menu links styling */
.nav-menu .menu-links {
  background-color: white;
}

.nav-menu .menu-links:not(:first-child) {
  border-top: #606060 solid 1px;
}

.menu-link {
  width: 200px;
  color: #606060;
}

.menu-link-large {
  height: fit-content !important;
}

/* Styling for the website body */
.main-body {
  height: calc(100vh - 57px);
  width: 100%;
  overflow-y: auto;
  float: left;
  position: relative;
}

</style>
<style>

/* Global color palette */
:root {
  --primary-color: #014878; /*014878*/
  --secondary-color: #35B1ECFF; /*35B1ECFF*/
  --tertiary-color-light: #D2ECF8FF;
  --tertiary-color-dark: #1976D2FF  ;
}

/* Body background color */
body {
  background: var(--primary-color);
}

/* Border radius for the graph plots*/
.main-svg {
  border-radius: 4px;
}

/* Overwrite default Vuetify font */
.v-application {
  font-family: "Inter", serif !important;
}

</style>