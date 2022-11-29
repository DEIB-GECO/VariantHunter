<template>
  <div :class="floating?'floating-intro':''">
    <template>
      <v-expand-transition>
        <v-alert v-if="showTip" color="#cf5832" dark dense
                 :icon="this.$vuetify.breakpoint.smAndDown?undefined:this.icon" prominent
                 :border="floating?'right':'left'" elevation="10" :max-height="floating?'45vh':undefined"
                 :max-width="floating?'80vw':undefined" :width="floating?'550px':undefined"
                 :class="'overflow-scroll pb-3 pt-6 px-7 rounded-xl '+(floating?'rounded-r-0':'bg_var2 text_var1--text rounded-l-0')"
                 :colored-border="!floating">
          <slot></slot>
          <div class="text-right pl-4 mt-6">
            <btn-with-tooltip :text="beginning?'Skip':'End tour'" icon="mdi-debug-step-over" :click-handler="terminate" hover-color="error"
                              size="small" content-class="ml-1 mt-1 mt-md-0" :bottom="!floating" :top="floating"
                              tip="I already know how the tool works"/>
            <btn-with-tooltip :text="this.beginning?'Start':this.end?'Okay':'Next'" :icon="end?'mdi-check':'mdi-chevron-right'"
                              :click-handler="showNext" hover-color="success"
                              size="small" content-class="ml-1 mt-1 mt-md-0" append-icon :bottom="!floating"
                              :top="floating" :tip="this.end?'End tour':'Next step'"/>
          </div>
        </v-alert>
      </v-expand-transition>
    </template>
  </div>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import {mapStateTwoWay} from "@/utils/bindService";

export default {
  name: "FeatureIntro",
  components: {BtnWithTooltip},
  props: {
    value: {},
    floating: Boolean,
    step: {},
    beginning: Boolean,
    end:Boolean,
    nextStep: {},
    altStep:{},
    icon: {},
    internalSteps:{default:0},
  },
  data(){
    return{
      nextPressCount: 0
    }
  },
  computed: {
    ...mapStateTwoWay({'tourStep': 'setTourStep'}),

    showTip() {
      return this.tourStep === this.step || (this.altStep && this.altStep === this.step)
    }
  },
  watch:{
    showTip(newVal){
      this.$emit('input',newVal)
    }
  },
  methods: {
    terminate() {
      this.tourStep = null
    },

    showNext() {
      if(this.internalSteps===this.nextPressCount) {
        console.log("Switch to " + this.nextStep)
        this.tourStep = this.nextStep
        this.$emit('nextStep')
      } else{
        this.nextPressCount++
        this.$emit('nextInternalStep')
      }
    }
  },
}
</script>

<style scoped>
.floating-intro {
  position: fixed;
  z-index: 8;
  bottom: 5px;
  right: 15px;
}
</style>