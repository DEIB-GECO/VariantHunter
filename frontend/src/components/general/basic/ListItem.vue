<template>
    <v-list-item :class="dense?'':'taller-list-item'" :link="link" @mouseenter="showTip=true" @mouseleave="showTip=false">
      <v-list-item-icon class="align-middle">
        <v-icon>{{icon}}</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="text-body-2 font-weight-bold">{{title}}</v-list-item-title>
        <v-expand-transition>
          <v-list-item-subtitle v-if="showTip || !expandOnHover" class="text-body-3">{{subtitle}}</v-list-item-subtitle>
        </v-expand-transition>
      </v-list-item-content>
      <v-list-item-action v-if="withActions"><slot name="actions"></slot></v-list-item-action>
    </v-list-item>
</template>


<script>
export default {
  name: "ListItem",
  props:{
    link:Boolean,
    expandOnHover: Boolean,
    subtitle:{},
    dense: Boolean,
    withActions: Boolean,
    title:{},
    icon:{}
  },
  data(){
    return {
      showTip:false
    }
  }
}
</script>

<style scoped>
.align-middle{
  margin-bottom: auto !important;
  margin-top: auto !important;
}
</style>
<style>
.taller-list-item{
  height: 56px;
}
</style>