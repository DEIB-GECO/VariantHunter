<template>
  <div>
    <v-btn x-small outlined depressed rounded color='primary' @click="showMenu=true">
      <v-icon x-small v-if="icon" left>{{icon}}</v-icon>
      {{text}}
    </v-btn>

    <v-menu v-model="showMenu" attach max-width="300">
      <v-list dense three-line>
        <v-list-item-group>
          <v-list-item v-for="(option, index) in options" :key="index" @click="onSelected(option.value)" dense>
            <v-list-item-icon>
              <v-icon  v-if="option.icon" v-text="option.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="option.text" class="text-left"></v-list-item-title>
              <v-list-item-subtitle v-if="option.description" v-text="option.description" class="option-subtitle text-left"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "MenuButton",
  props:{
    icon:{},
    text:{},
    options:{},
  },
  data(){
    return{
      showMenu:false,
    }
  },
  methods:{
    onSelected(value){
      this.showMenu=false
      this.$emit("select",value)
    }
  }
}
</script>

<style scoped>
.option-subtitle{
  font-size: 12px !important;
  line-height: 13px !important;
  -webkit-line-clamp: inherit !important;
}
</style>