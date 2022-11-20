<template>
  <v-tooltip :disabled="tip===''"  :bottom="bottom" content-class="rounded-xl tooltip"  :left="left" :right="right" :top="top" allow-overflow z-index="999" max-width="400px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn depressed :outlined="outlined" rounded :small="size==='small'" :x-small="size==='x-small'" :dark="dark" :class="contentClass"
             :color="(isHover && hoverColor)?hoverColor:color" v-bind="attrs" v-on="on" @click.stop="onClick()"
             @mouseenter="isHover=true" @mouseleave="isHover=false">
        <slot name="btn">
          <v-icon v-if="!appendIcon" :small="size==='small'" :x-small="size==='x-small'" left :dark="dark">
            {{ icon }}
          </v-icon>
          {{ text }}
          <v-icon v-if="appendIcon" :small="size==='small'" :x-small="size==='x-small'" right  :dark="dark">
            {{ icon }}
          </v-icon>
        </slot>
      </v-btn>
    </template>
    <span class="compact-tooltip">
      <slot name="tip">
        <span v-html="tip"/>
      </slot>
    </span>
  </v-tooltip>
</template>

<script>
export default {
  name: "BtnWithTooltip",
  props: {
    contentClass:{},
    color: {},
    hoverColor: {},
    text: {},
    icon: {},
    dark: Boolean,
    tip: {},
    size: {},
    left: Boolean,
    right: Boolean,
    top: Boolean,
    outlined: Boolean,
    bottom: Boolean,
    clickHandler: {},
    appendIcon: Boolean,
  },
  data() {
    return {
      isHover: false
    }
  },
  methods: {
    onClick() {
      if (this.clickHandler)
        this.clickHandler()
    }
  }
}
</script>

<style scoped>

</style>

<style>


</style>