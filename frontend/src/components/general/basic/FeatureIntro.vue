<!--

  Component:    FeatureIntro
  Description:  Component for app tour to illustrate the potential of the tool

  Props:
  ├── value:          Value for the binding of the visibility
  ├── floating:       Boolean flag set to true
  ├── step:           Step name
  ├── altSteps:       Alternative step names
  ├── nextStep:       Next step name or null
  ├── beginning:      Boolean flag set to true if the step begin the tour
  ├── end:            Boolean flag set to true if the step ends the tour
  ├── icon:           Step icon
  └── internalSteps:  Number of internal steps

  Slots:
  └── default:            Default slot

  Events:
  ├── nextStep:           Emitted on next tour step
  └── nextStepInternal:   Emitted on next internal tour step

-->

<template>
  <div :class="floating?'floating-intro':''">
    <template>
      <v-expand-transition>
        <v-alert v-if="showTip" color="#cf5832" dark dense
                 :icon="this.$vuetify.breakpoint.smAndDown?undefined:this.icon" prominent
                 :border="floating?'right':'left'" elevation="10" :max-height="floating?'45vh':undefined"
                 :max-width="floating?'80vw':undefined" :width="floating?'550px':undefined"
                 :class="'overflow-scroll pb-3 pt-6 px-7 rounded-xl '+(floating?'rounded-r-0':'bg_var3 f_text_dark--text rounded-l-0')"
                 :colored-border="!floating">

          <!-- Tour step content -->
          <slot></slot>

          <!-- Actions -->
          <div class="text-right pl-4 mt-6">
            <btn-with-tooltip v-if="!lastStep" :text="beginning?'Skip':'End tour'" icon="mdi-debug-step-over"
                              :click-handler="terminate" hover-color="error"
                              size="small" content-class="ml-1 mt-1 mt-md-0" :bottom="!floating" :top="floating"
                              tip="I already know how the tool works"/>
            <btn-with-tooltip :text="this.beginning?'Start':this.lastStep?'Okay':'Next'"
                              :icon="this.lastStep?'mdi-check':'mdi-chevron-right'"
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
    /** Value for the binding of the visibility */
    value: {},

    /** Boolean flag set to true */
    floating: Boolean,

    /** Step name */
    step: {},

    /** Alternative step names */
    altSteps: {},

    /** Next step name or null */
    nextStep: {},

    /** Boolean flag set to true if the step begin the tour */
    beginning: Boolean,

    /** Boolean flag set to true if the step ends the tour*/
    end: Boolean,

    /** Step icon */
    icon: {},

    /** Number of internal steps */
    internalSteps: {default: 0},
  },

  data() {
    return {
      /** Counter of clicks on next button */
      nextPressCount: 0
    }
  },

  computed: {
    ...mapStateTwoWay({'tourStep': 'setTourStep'}),

    /** Visibility flag for the tip */
    showTip() {
      return this.tourStep === this.step || (this.altSteps && this.altSteps.includes(this.tourStep))
    },

    /** Boolean flag set to true if the tour-step ends the tour */
    lastStep() {
      return this.internalSteps === this.nextPressCount && this.end
    }
  },

  watch: {
    showTip(newVal) {
      this.$emit('input', newVal)
    }
  },

  methods: {
    /** Skip the tour */
    terminate() {
      this.tourStep = null
    },

    /** Go to the next step */
    showNext() {
      if (this.internalSteps === this.nextPressCount) {
        this.tourStep = this.nextStep
        this.$emit('nextStep')
      } else {
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