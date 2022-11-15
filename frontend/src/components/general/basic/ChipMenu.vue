<template>
  <v-menu v-model="showMenu"  rounded :attach="attach" offset-y :close-on-content-click="closeOnContentClick" >
    <template v-slot:activator="{ on, attrs }">
      <v-chip :small="small" dark :color="color" :outlined="activatorOutlined" :class="'text-uppercase'"
              v-bind="attrs" v-on="on">
        <v-icon left :small="small">{{ activatorIcon }}</v-icon>
        {{ activatorText }}
      </v-chip>
    </template>
    <v-card class="f_text_dark--text" rounded max-width="300px" color="f_tertiary" @mouseleave="onMouseLeave">
      <v-container>
        <slot></slot>
      </v-container>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "ChipMenu",
  props: {
    activatorText: {},
    activatorIcon: {},
    activatorOutlined: {default: true},
    small: Boolean,
    closeOnContentClick: {default: true},
    color: {default: 'tertiary'},
    tile: Boolean,
    attach:{},
    hideOnLeave: Boolean,
  },
  data(){
    return{
      showMenu:false,
    }
  },
  methods:{
    onMouseLeave(){
      if(this.hideOnLeave){
        this.showMenu=false
      }
    }
  }
}
</script>

<style scoped>

</style>