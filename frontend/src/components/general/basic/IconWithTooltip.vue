<template>
  <v-tooltip :disabled="tip===''" :bottom="bottom" :left="left" :right="right" :top="top" allow-overflow z-index="10" :close-delay="0">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon :small="size==='small'" :color="(isHover && hoverColor)?hoverColor:color" v-bind="attrs" v-on="on" @click.stop="onClick()" @mouseenter="isHover=true" @mouseleave="isHover=false">
            <v-icon  :color="(isHover && hoverColor)?hoverColor:color" :size="size" :dark="dark" >
            {{icon}}
            </v-icon>
          </v-btn>
        </template>
      <slot name="tip">
        <span>{{tip}}</span>
      </slot>
  </v-tooltip>
</template>

<script>
export default {
  name: "IconWithTooltip",
  props:{
    color:{default:''},
    hoverColor:{},
    icon:{},
    dark:Boolean,
    tip:{},
    size:{},
    left:Boolean,
    right:Boolean,
    top:Boolean,
    bottom:Boolean,
    clickHandler:{}
  },
  data(){
    return {
      isHover: false
    }
  },
  methods:{
    onClick(){
      if(this.clickHandler)
        this.clickHandler()
    }
  }
}
</script>

<style scoped>

</style>