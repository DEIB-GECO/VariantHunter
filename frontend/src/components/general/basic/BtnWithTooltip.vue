<template>
  <v-tooltip :bottom="bottom" :left="left" :right="right" :top="top" allow-overflow z-index="10">
    <template v-slot:activator="{ on, attrs }">
      <v-btn depressed :outlined="outlined" rounded :small="size==='small'" :dark="dark"
             :color="(isHover && hoverColor)?hoverColor:color" v-bind="attrs" v-on="on" @click.stop="onClick()"
             @mouseenter="isHover=true" @mouseleave="isHover=false">
        <v-icon v-if="!appendIcon" left :size="size" :dark="dark">
          {{ icon }}
        </v-icon>
        {{ text }}
        <v-icon v-if="appendIcon" right :size="size" :dark="dark">
          {{ icon }}
        </v-icon>
      </v-btn>
    </template>
    <slot name="tip">
      <span>{{ tip }}</span>
    </slot>
  </v-tooltip>
</template>

<script>
export default {
  name: "BtnWithTooltip",
  props: {
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