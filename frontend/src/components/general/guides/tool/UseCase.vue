<!--
  Component:    UseCase
  Description:  Use case section

  Props:
  └── name:     Title for the use case

  Slots:
  └── default:  Content of the use case section
-->

<template>
  <v-expansion-panel>
    <v-expansion-panel-header class='grey lighten-5'>
      <v-col class='col-auto'>
        <v-icon left color='black'>mdi-lightbulb-on-outline</v-icon>
      </v-col>
      <v-col>
        {{ name }}
      </v-col>
    </v-expansion-panel-header>
    <v-expansion-panel-content class='grey lighten-5'>
      <slot>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
        ut
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
        cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      </slot>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: 'UseCase',
  props: {
    /** Title for the use case */
    name: {}
  }
}
</script>

<style scoped>

</style>
