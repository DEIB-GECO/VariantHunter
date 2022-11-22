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
    <div v-if="!useLocalOpt">
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="warning" color="tertiary"
                        icon="mdi-filter-off" text="Switch to local filtering scope" bottom :click-handler="disableTagFilters"
                        tip="Use local filters for this analysis instead of the tag-based ones"/>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="error" color="tertiary"
                        icon="mdi-filter-remove" text="Clear filters" bottom :click-handler="()=>clearFilters(false)"
                        tip="Clear the filtering options for all the analysis belonging to this tag group"/>
    </div>
    <div v-else>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="error" color="tertiary"
                        icon="mdi-filter-remove" text="Clear filters" bottom :click-handler="()=>clearFilters(true)"
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
    ...mapGetters(['useLocalOpt']),
  },
  methods:{
    ...mapMutations(['setOpt']),

    /**
     * Clear filters of a given scope
     * @param local  True iff the filtering scope to be cleared is the local one.
     */
    clearFilters(local){
      this.setOpt({local,opt:'protein',value:null})
      this.setOpt({local,opt:'muts',value:[]})
      this.setOpt({local,opt:'rowKeys',value:[]})
    },

    /**
     * Change the filtering scope of the current analysis from tag-based to local
     */
    disableTagFilters(){
      this.setOpt({local:true,opt:'useLocalOpt',value:true})
    }
  }
}
</script>

<style scoped>

</style>