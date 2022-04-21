<!--
  Component:    ToolGuide
  Description:  Usage guide for the tool
-->

<template>
  <v-container class='mt-10'>
    <h3 id='docker_guide'>
      <v-icon left color='#000000DE' large>mdi-human-greeting</v-icon>
      What is VariantHunter
    </h3>
    <p class='pl-10 pr-10'>
      <i>VariantHunter</i> is a tool for fast detection of emerging <i>SARS-CoV-2</i> variants. <br />It's an highly
      flexible and user friendly application for the systematic monitoring of the evolution of <i>SARS-CoV-2</i> both at
      global and regional level.
    </p>
    <v-container class='pl-10 pr-10 pb-5' v-if='!collapsed'>

      <v-expansion-panels class='mt-3' flat>

        <!-- LINEAGE INDEPENDENT -->
        <v-expansion-panel>
          <v-expansion-panel-header class='blue-grey lighten-5'><b>
            <v-icon left color='black'>mdi-star-circle-outline</v-icon>
            Discover the lineage-independent search</b></v-expansion-panel-header>
          <v-expansion-panel-content class='blue-grey lighten-5'>
            <template>
              <v-row>
                <v-col class='col-sm-6'>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                  </p>
                </v-col>
                <v-col class='col-sm-6'>
                  <img width='400'
                       src='https://macostutorial.com/EN-MACOS-6a-safari/Screenshot_2021-02-18_at_21.55.35.png' />
                </v-col>
              </v-row>
              <v-row>
                <v-col class='col-sm-6'>
                  <img width='400'
                       src='https://macostutorial.com/EN-MACOS-6a-safari/Screenshot_2021-02-18_at_21.55.35.png' />
                </v-col>
                <v-col class='col-sm-6'>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                  </p>
                </v-col>
              </v-row>
              <v-row class='ma-10'>
                <v-expansion-panels class='mt-3' flat>

                  <v-expansion-panel>
                    <v-expansion-panel-header class='grey lighten-5'><b>
                      <v-icon left color='black'>mdi-lightbulb-on-outline</v-icon>
                      Use case 1</b></v-expansion-panel-header>
                    <v-expansion-panel-content class='grey lighten-5'>
                      <template>
                        <v-row>
                <v-col class='col-sm-6'>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                  </p>
                </v-col>
                <v-col class='col-sm-6'>
                  <img width='400'
                       src='https://macostutorial.com/EN-MACOS-6a-safari/Screenshot_2021-02-18_at_21.55.35.png' />
                </v-col>
              </v-row>
              <v-row>
                <v-col class='col-sm-6'>
                  <img width='400'
                       src='https://macostutorial.com/EN-MACOS-6a-safari/Screenshot_2021-02-18_at_21.55.35.png' />
                </v-col>
                <v-col class='col-sm-6'>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                    laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                  </p>
                </v-col>
              </v-row>
                      </template>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel>
                    <v-expansion-panel-header class='grey lighten-5'><b>
                      <v-icon left color='black'>mdi-lightbulb-on-outline</v-icon>
                      Use case 2</b></v-expansion-panel-header>
                    <v-expansion-panel-content class='grey lighten-5'>
                      <template>
                      </template>
                    </v-expansion-panel-content>
                  </v-expansion-panel>

                </v-expansion-panels>

              </v-row>

            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header class='blue-grey lighten-5'><b>
            <v-icon left color='black'>mdi-star-circle-outline</v-icon>
            Discover the lineage-specific search</b></v-expansion-panel-header>
          <v-expansion-panel-content class='blue-grey lighten-5'>
            ---
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-container>
    <v-container class='pl-10 pr-10'>
      <v-btn v-if='collapsed' class='full-width-button black--text' @click.native='collapsed=false' color='#e0e0e0'
             large depressed outlined rounded>
        <v-icon left>mdi-plus</v-icon>
        <span class='black--text'>Show tool guide</span>
      </v-btn>
      <v-btn v-else class='full-width-button black--text' @click.native='collapsed=true' color='#e0e0e0' depressed
             outlined rounded>
        <v-icon left>mdi-minus</v-icon>
        <span class='black--text'>collapse</span>
      </v-btn>
    </v-container>
  </v-container>
</template>

<script>
import CodeBlock from '@/components/general/CodeBlock'

export default {
  name: 'ToolGuide',
  components: { CodeBlock },
  data () {
    return {
      /** Flag to show/hide the advanced otional params */
      showAllParams: false,

      /** Flag to show/hide the whole section*/
      collapsed: true
    }
  }
}
</script>

<style scoped>

/** Requirement red list */
ul.red-list li::marker {
  color: #F44336;
}

/* Table styling */
tr td:first-child, .monospaced {
  font-family: monospace !important;
}

.table-with-borders {
  border: thin solid rgba(0, 0, 0, 0.12) !important;
  border-radius: var(--border-radius) !important;
}

tbody tr td {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
  font-size: 14px !important;
}

tbody tr td:first-child {
  font-weight: bold;
}

.alternate-rows tr:nth-child(2n) {
  background: #f6f6f6;
}

.alternate-rows * :hover {
  background: #e0e0e0 !important;
}

.expand-table, .expand-table > *:hover {
  background: white !important;
}

.full-width-button {
  width: 100% !important;
}

</style>
