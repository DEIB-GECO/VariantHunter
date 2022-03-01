<template>
  <v-app>

    <!-- Navbar -->
    <v-toolbar :color="primary_color" class="navbar" dark>

      <!-- Logo -->
      <v-img :src="websiteLogo" contain max-height="39px" max-width="39px"/>
      <v-toolbar-title class="headline">
        <span>Variant</span>
        <span class="font-weight-light"> Hunter</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>


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

    <v-main>
      <MenuPage></MenuPage>
    </v-main>

  </v-app>
</template>

<script>

import {mapState} from "vuex";
import MenuPage from "@/components/MenuPage";

export default {
  components: {
    MenuPage
  },

  data() {
    return {
      /** VariantHunter logo */
      websiteLogo: require('./images/virusurf_logo.png'),
    }
  },
  computed: {
    ...mapState(['primary_color']),
  }
};

</script>

<style scoped>

.navbar {
  width: 100%;
  max-height: 65px;
}

.headline {
  font-size: 32px !important;
  margin-left: 20px;
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

</style>
<style>
.main-svg{
  border: 1px solid grey;
  border-radius: 4px;
}
</style>