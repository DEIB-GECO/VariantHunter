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
    <div>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="warning" color="tertiary"
                        icon="mdi-filter-off" text="Disable filters locally" bottom
                        tip="Use local filters for this analysis instead of the global ones"/>
      <btn-with-tooltip size="x-small" content-class="my-1  mx-auto d-block" hover-color="error" color="tertiary"
                        icon="mdi-filter-remove" text="Remove filters" bottom
                        tip="Remove filters for all the performed analysis"/>
    </div>
  </div>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";

export default {
  name: "EmptyTable",
  components: {BtnWithTooltip}
}
</script>

<style scoped>

</style>