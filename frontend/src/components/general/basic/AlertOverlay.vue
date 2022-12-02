<template>
  <v-overlay :value="value">
    <v-alert v-click-outside="hide" prominent :type="type" :icon="icon" max-width="70vw" width="800px"
             class="py-10 px-7 rounded-xl rounded-l-0 bg_var2 text_var1--text" border="left" colored-border>
      <div class="pl-4">
        <slot></slot>
      </div>
      <div class="text-right pl-4 mt-6">
        <v-btn rounded elevation="0" @click="hide">Okay</v-btn>
      </div>
    </v-alert>
  </v-overlay>
</template>

<script>
export default {
  name: "AlertOverlay",
  props: {
    value: {},
    icon: {},
    type: {}
  },
  methods: {
    hide() {
      this.$emit('input', false)
    }
  }
}
</script>

<style scoped>

</style>