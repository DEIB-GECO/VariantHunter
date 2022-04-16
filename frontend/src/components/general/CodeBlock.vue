<!--
  Component:    CodeBlock
  Description:  Code block with copy button

  Props:
  └── code:  The content of the code block
-->

<template>
  <code @click='doCopy()'>
    {{code}}
    <v-icon small class='ml-3'>mdi-content-copy</v-icon>
    <v-snackbar v-model='successMessage' timeout='2000' height='5' color='success' transition='scroll-y-transition'>
      <v-icon left>mdi-content-copy</v-icon>
      <span><b>Copied to clipboard!</b></span>
    </v-snackbar>
  </code>

</template>

<script>
export default {
  name: 'CodeBlock',
  props: {
    code: { required: true }
  },
  data () {
    return {
      /** Success message for the copy action */
      successMessage: false
    }
  },
  methods: {
    /**
     * Copy the element content
     * @param e The copy event
     */
    doCopy (e) {
      this.$copyText(this.code).then(() => { this.successMessage = true })
    }
  }
}
</script>

<style scoped>
code{
  cursor: copy;
  font-size: 16px;

}
</style>
