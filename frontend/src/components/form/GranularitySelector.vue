<!--

  Component:    GranularitySelector
  Description:  Select input element for the granularity of analysis.

-->

<template>
  <FieldSelector v-model='selectedGranularity' :possible-values='possibleGranularity'
                 label='Granularity' placeholder='Granularity' solo />
</template>

<script>
import FieldSelector from '@/components/form/FieldSelector'
import { mapState } from 'vuex'
import { mapStateTwoWay } from '@/utils/bindService'

export default {
  name: 'GranularitySelector',
  components: { FieldSelector },
  computed: {
    ...mapState(['possibleGranularity']),
    ...mapStateTwoWay({ selectedGranularity: 'SET_GRANULARITY' })
  }
}

</script>
