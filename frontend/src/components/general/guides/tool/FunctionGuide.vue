<!--
  Component:    FunctionGuide
  Description:  Guide for a specific function

  Props:
  ├── title:      Title for the panel header
  └── noUseCases: If true, no use case section

  Slots:
  ├── default:    Content of the function intro
  └── use-cases:  Content of the use case section
-->

<template>
  <v-expansion-panel>
    <v-expansion-panel-header class='blue-grey lighten-5'>
      <v-col class='col-auto'>
        <v-icon left color='black'>mdi-star-circle-outline</v-icon>
      </v-col>
      <v-col>
        {{title}}
      </v-col>
    </v-expansion-panel-header>
    <v-expansion-panel-content class='blue-grey lighten-5'>
      <template>

        <!-- INTRO -->
        <slot>
        </slot>

        <!-- USE CASES -->
        <v-row v-if="!noUseCases" class='ma-10'>
          <v-expansion-panels class='mt-3' flat>

            <slot name='use-cases'>
            </slot>

          </v-expansion-panels>

        </v-row>

      </template>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: 'FunctionGuide',
  props: {
    /** Title for the panel header */
    title: {},

    /** If true, no use case section */
    noUseCases: Boolean
  }
}
</script>

<style scoped>

</style>
