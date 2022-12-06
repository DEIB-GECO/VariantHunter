<!--

  Component:    ExpansionModeMenu
  Description:  Component to change aggregation mode for the expanded row

  Props:
  └── value: Value of the aggregation mode

-->

<template>
  <v-card width="90%" class="options text-left" color="transparent" flat>

    <!-- Headings -->
    <div class="options-intro">
      <div class="main">Lineages breakdown</div>
      computed considering the expanded mutation in the 4 weeks and location
    </div>

    <!-- Aggregation options menu -->
    <v-menu v-model="showOptions" content-class="rounded-xl navbar-menu" offset-y open-on-click width="250px"
            max-width="80vw" :open-on-hover="false" close-on-content-click>

      <!-- Activator: button -->
      <template v-slot:activator="{ attrs, on }">
        <span v-bind="attrs" v-on="on">
          <btn-with-tooltip bottom color="primary" outlined hover-color="warning" size="x-small"
                            :icon="notationOptions[notationMode].icon" text="Change notation"
                            :tip="showOptions?'':'Change the notation for the lineages by defining the level of aggregation'"
                            :click-handler="()=>showOptions=!showOptions"/>
        </span>
      </template>

      <!-- Actual menu with aggregation options-->
      <div @mouseleave="showOptions=false">
        <v-list color="bg_var1" rounded dense width="auto">
          <v-list-item v-for="[key,opt] in Object.entries(notationOptions)" :key="key" link dense
                       @click="changeNotationMode(key)" :class="(key===notationMode)?'v-list-item--active':''">
            <v-icon class="pr-3" color="primary">{{ opt.icon }}</v-icon>
            <v-list-item-content>
              <v-list-item-title class="primary--text">{{ opt.text }}</v-list-item-title>
              <v-list-item-subtitle v-html="opt.description" class="break-spaces"/>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
    </v-menu>
  </v-card>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip.vue";

export default {
  name: "ExpansionModeMenu",
  components: {BtnWithTooltip},

  props: {
    /** Value of the aggregation mode */
    value: {},
  },

  data() {
    return {
      /** Boolean visibility flag for the aggregation options menu */
      showOptions: false,

      /** Possible aggregation options */
      notationOptions: {
        1: {
          text: 'Use simplified notation (level 1)',
          description: 'Summarize the counts using a level-1 star notation for the lineages (e.g., B.1.*). <br/>' +
              'In any case, lineages exceeding 10% spread will not be aggregated',
          icon: 'mdi-minus'
        },
        2: {
          text: 'Use simplified notation (level 2)',
          description: 'Summarize the counts using a level-2 star notation for the lineages (e.g., B.1.1.*). <br/>' +
              'In any case, lineages exceeding 10% spread will not be aggregated',
          icon: 'mdi-equal'
        },
        0: {
          text: 'Use complete notation',
          description: 'Differentiate each lineage (e.g.: B.1.1, B.1.2,...) by avoiding groupings.',
          icon: 'mdi-text-long'
        },
      }
    }
  },

  computed: {

    /** Current value of aggregation mode */
    notationMode: {
      set(newVal) {
        this.$emit('input', Number(newVal))
      },
      get() {
        return String(this.value)
      }
    },
  },

  methods: {
    /**
     * Change notation mode
     * @param e The selected mode
     */
    changeNotationMode(e) {
      this.notationMode = e
    }
  }
}
</script>

<style scoped>
.options {
  padding-left: 35px;
  position: absolute;
  top: 0;
}

.options-intro {
  max-width: 170px;
  padding-top: 13px;
  margin-bottom: 10px;
  color: var(--v-text_var1-base);
  font-weight: normal;
  font-size: 12px;
  line-height: 13px;
  letter-spacing: 0.019em;
}

.options-intro .main {
  font-weight: bold;
}
</style>