<template>
  <div class="my-8">
    <v-list class="mx-auto text-center" width="fit-content" color="transparent">
      <v-list-item>
        <v-list-item-icon>
          <v-icon class="d-block mb-2" color="error">mdi-file-remove-outline</v-icon>
        </v-list-item-icon>
        <span class="text-body-3 error--text">No mutations matching the selected filters.</span>
      </v-list-item>
    </v-list>
    <div v-if="useGlobalFilters">
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="warning" color="tertiary"
                        icon="mdi-filter-off" text="Switch to local filtering scope" bottom :click-handler="disableGlobalFilters"
                        tip="Use local filters for this analysis instead of the global ones"/>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="error" color="tertiary"
                        icon="mdi-filter-remove" text="Clear filters" bottom :click-handler="()=>clearFilters(true)"
                        tip="Clear the global filtering options for all the analysis (this, the others and future ones)"/>
    </div>
    <div v-else>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="error" color="tertiary"
                        icon="mdi-filter-remove" text="Clear filters" bottom :click-handler="()=>clearFilters(false)"
                        tip="Clear local filters"/>
    </div>
  </div>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "EmptyTable",
  components: {BtnWithTooltip},
  computed:{
    ...mapGetters(['getCurrentLocalFilteringOpt']),

    useGlobalFilters(){
      return  this.getCurrentLocalFilteringOpt.useGlobalFilters
    },
  },
  methods:{
    ...mapMutations(['setFilterOpt']),

    /**
     * Clear filters of a given scope
     * @param global  True iff the filtering scope to be cleared is the global one.
     */
    clearFilters(global){
      this.setFilterOpt({global,opt:'protein',value:null})
      this.setFilterOpt({global,opt:'muts',value:[]})
      this.setFilterOpt({global,opt:'rowKeys',value:[]})
    },

    /**
     * Change the filtering scope of the current analysis from global to local
     */
    disableGlobalFilters(){
      this.setFilterOpt({global:false,opt:'useGlobalFilters',value:false})
    }
  }
}
</script>

<style scoped>

</style>