<!--
  Component:    UseCase
  Description:  Use case section

  Props:
  ├── name:         Title for the use case
  ├── sourceName:   Source information for the use cases: name of the source
  └── sourceDate:   Source information for the use cases: date of the source

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
      <v-tooltip bottom max-width='600' :color="f_primary" open-delay='0' content-class='small-hint'>
          <template v-slot:activator="{ on, attrs }">
            <div class='source' v-bind="attrs" v-on="on">
             Data from {{sourceName}} dated {{sourceDate}}
            </div>
          </template>
          <span>
            This use case is based on the analysis of the data contained
            in the metadata.tsv file published by {{sourceName}} on {{sourceDate}}.<br/>
            Find out how to download it from the Docker Guide below.
          </span>
        </v-tooltip>
    </template>

    <template v-slot:default>
      <div class='mt-2'>
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
        </div>
    </template>

  </ExpansionPanel>
</template>

<script>
import ExpansionPanel from '@/components/general/basic/ExpansionPanel'
import { mapState } from 'vuex'
export default {
  name: 'UseCase',
  components: { ExpansionPanel },
  props: {
    /** Title for the use case */
    name: { required: true },

    /** Source information for the use cases: name of the source */
    sourceName: { required: true },

    /** Source information for the use cases: date of the source */
    sourceDate: { required: true }
  }
}
</script>

<style scoped>

/** Source info label */
.source{
  margin-top: 5px;
  font-size: 11px;
  font-weight: 300 !important;
  width: fit-content;
}
.small-hint{
  line-height: 15px !important;
}
</style>
