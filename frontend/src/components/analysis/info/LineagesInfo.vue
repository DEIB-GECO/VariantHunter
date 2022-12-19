<!--

  Component:    LineagesInfo
  Description:  Lineages info summary of the result panel of a lineage specific-analysis

-->

<template>
  <v-list color="transparent">
    <v-list-item>

      <v-list-item-icon>
        <v-icon left large color="primary">mdi-source-branch</v-icon>
      </v-list-item-icon>

      <v-tooltip top right allow-overflow z-index="999" :close-delay="0" max-width="400px" :open-delay="600">
        <!-- Activator: section name-->
        <template v-slot:activator="{ on, attrs }">
          <v-list-item-content v-on="on" v-bind="attrs">
            <v-list-item-title>Analyzed lineages
            </v-list-item-title>
            <v-list-item-subtitle class="break-spaces">{{ lineagesText }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </template>

        <!-- Lineages info on hover -->
        <div class="pa-3">
          <div class="text-body-3 font-weight-bold mb-3">
            <v-icon left color="f_text_light">mdi-source-branch</v-icon>
            Lineages considered for this analysis
          </div>
          <div class="mb-3" v-if="lineageItems.length>0">
            <v-chip v-for="item in lineageItems" :key="item" :color="getLineageColor(item).color"
                    :light="!getLineageColor(item).isDark" :dark="getLineageColor(item).isDark" small
                    class="mr-1 mb-1">{{ item }}
            </v-chip>
          </div>
          <div class="mb-3" v-for="[groupName,groupItems] in lineageGroups" :key="groupName">
            <div class="mb-1">
              <v-chip :color="getLineageColor(groupName).color" :light="!getLineageColor(groupName).isDark"
                      :dark="getLineageColor(groupName).isDark" small>{{ groupName }}
              </v-chip>
              <span class="text-body-5">, specifically:</span>
            </div>
            <div class="ml-3" v-if="groupItems?.length>0">
              <v-chip v-for="item in groupItems" :key="item" :color="getLineageColor(item).color"
                      :light="!getLineageColor(item).isDark" :dark="getLineageColor(item).isDark" x-small
                      class="mr-1 mb-1">{{ item }}
              </v-chip>
            </div>
            <div v-else class="ml-3 text-body-5">None (completely absent)</div>
          </div>
        </div>

      </v-tooltip>

    </v-list-item>
  </v-list>
</template>

<script>
import {toText} from "@/utils/formatterService";
import {mapGetters} from "vuex";
import {getRandomColor} from "@/utils/colorService";

export default {
  name: "LineagesInfo",

  data() {
    return {
      /** Object storing lineage colors*/
      lineageColors: {},
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    /** Mapping lineage toText */
    lineagesText() {
      return toText(this.getCurrentAnalysis.query.lineage)
    },

    /** List of well-defined lineages */
    lineageItems() {
      return this.getCurrentAnalysis.query.lineage.items
    },

    /** List of lineages in star notation */
    lineageGroups() {
      return Object.entries(this.getCurrentAnalysis.query.lineage.groups)
    }
  },

  methods: {
    /** Get a random color to be associated with the lineage */
    getLineageColor(lineage) {
      if (!this.lineageColors[lineage])
        this.lineageColors[lineage] = getRandomColor()
      return this.lineageColors[lineage]
    }
  }
}
</script>

<style scoped>

</style>