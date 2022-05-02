<!--
  Component:    UseCase
  Description:  Use case section

  Props:
  └── name:     Title for the use case

  Slots:
  └── default:  Content of the use case section
-->

<template>
  <ExpansionPanel>

    <template v-slot:icons>
      <v-icon left color='#000000DE'>mdi-lightbulb-on-outline</v-icon>
    </template>

    <template v-slot:title>
      <span v-html='name'></span>
    </template>

    <template v-slot:default>
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
    </template>

  </ExpansionPanel>
</template>

<script>
import ExpansionPanel from '@/components/general/ExpansionPanel'
export default {
  name: 'UseCase',
  components: { ExpansionPanel },
  props: {
    /** Title for the use case */
    name: { required: true }
  }
}
</script>

<style scoped>

</style>
