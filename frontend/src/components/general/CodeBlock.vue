<!--
  Component:    CodeBlock
  Description:  Code block with copy button

  Props:
  ├── code:   The content of the code block
  └── hover:  The tip text to be shown on hover
-->

<template>
  <code @click='doCopy()'>
    <!-- Code with tooltip -->
    <v-tooltip v-if='hover' bottom color='black' max-width='400'>
      <template v-slot:activator="{ on, attrs }">
        <span v-bind="attrs"
          v-on="on">
        {{code}}
        </span>
      </template>
      <span v-html="hover"></span>
    </v-tooltip>
    <span v-else>{{code}}</span>
    <v-icon small class='ml-3'>mdi-content-copy</v-icon>

    <!-- Copied alert -->
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
    /** The content of the code block */
    code: { required: true },

    /** The tip text to be shown on hover */
    hover: { required: false }
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
    doCopy () {
      this.$copyText(thi  s.code).then(() => { this.successMessage = true })
    }
  }
}
</script>

<style scoped>
code{
  cursor: copy;
  font-size: 16px;
  word-spacing: 6px;
}
</style>
