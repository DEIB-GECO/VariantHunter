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
  <ExpansionPanel>

    <template v-slot:icons>
      <v-icon left color='#000000DE'>mdi-star-circle-outline</v-icon>
    </template>

    <template v-slot:title>
      <span v-html='title'></span>
    </template>

    <template v-slot:default>

      <!-- INTRO -->
      <slot>
      </slot>

      <!-- USE CASES -->
      <v-row v-if='!noUseCases' class='mt-10 mb-10 ml-0 mr-0'>
        <v-expansion-panels class='mt-3' flat>

          <slot name='use-cases'>
          </slot>

        </v-expansion-panels>

      </v-row>

    </template>
  </ExpansionPanel>
</template>

<script>
import ExpansionPanel from '@/components/general/ExpansionPanel'

export default {
  name: 'FunctionGuide',
  components: { ExpansionPanel },
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
