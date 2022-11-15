<!--
  Component:    ExpansionPanel
  Description:  Customized expansion panel

  Props:
  └── doubleIcon: Flag to reserve space for two icons in the name

  Slots:
  ├── title:    Slot for the title of the expansion panel
  ├── icons:    Slot for the icons of the expansion panel
  └── default:  Slot for the content of the expansion panel

-->

<template>
  <v-expansion-panel>

    <!-- Expansion panel header-->
    <v-expansion-panel-header>
      <v-col :class='"pa-0 pa-sm-auto col-auto "+ (doubleIcon?"larger-icon-section":"standard-icon-section")'>
        <slot name='icons'></slot>
      </v-col>
      <v-col class='pl-0 pl-sm-auto pr-0 pr-sm-auto'>
        <slot name='title'></slot>
      </v-col>
    </v-expansion-panel-header>

    <!-- Expansion panel content-->
    <v-expansion-panel-content>
      <slot></slot>
    </v-expansion-panel-content>

  </v-expansion-panel>
</template>

<script>
export default {
  name: 'ExpansionPanel',
  props: {
    /** Flag to reserve space for two icons in the name */
    doubleIcon: Boolean
  }
}
</script>

<style scoped>
.v-expansion-panel {
  border: 1px solid black;
  border-radius: 30px !important;
  margin-bottom: 10px;
}

.v-expansion-panel-header {
  font-size: 14px !important;
  text-transform: uppercase;
  font-weight: 500 !important;
  letter-spacing: 0.0892857143em;
}

.v-expansion-panel b {
  font-weight: bold !important;
}

.v-expansion-panel-header .col:first-child {
  display: inline-flex !important;
  justify-content: center;
}

.larger-icon-section{
  min-width: 104px !important;
  max-width: 104px !important;
}
.standard-icon-section{
  max-width: 48px !important;
}
</style>
