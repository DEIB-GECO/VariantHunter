<!--

  Component:    DockerGuide
  Description:  Container for the guides to install and run the docker

-->

<template>
  <v-container class='ml-0 ml-sm-auto mr-0 mr-sm-auto pt-5'>
    <h3>
      <v-icon left large color="text_var1">mdi-docker</v-icon>
      How to run the Docker
    </h3>
    <v-container class='pl-0 pl-sm-10 pr-0 pr-sm-10 pb-5'>

      <v-expansion-panels class='mt-3' flat>

        <!-- WINDOWS LINUX GUIDE -->
        <expansion-panel double-icon>
          <template v-slot:icons>
            <v-icon color="text_var1">mdi-microsoft</v-icon>
            <v-icon color="text_var1">mdi-slash-forward</v-icon>
            <v-icon left color="text_var1">mdi-penguin</v-icon>
          </template>
          <template v-slot:title>
            <span class='hidden-xs-only'>Instructions for </span> <b>Windows / Linux</b>
          </template>
          <template v-slot:default>
            <docker-guide-steps/>
          </template>
        </expansion-panel>

        <!-- MACOS GUIDE -->
        <expansion-panel double-icon>
          <template v-slot:icons>
            <v-icon left color='text_var1'>mdi-apple</v-icon>
          </template>
          <template v-slot:title>
            <span class='hidden-xs-only'>Instructions for </span> <b>MacOS</b>
          </template>
          <template v-slot:default>
            <docker-guide-steps mac-guide/>
          </template>
        </expansion-panel>

      </v-expansion-panels>
    </v-container>
  </v-container>
</template>

<script>
import DockerGuideSteps from '@/components/guides/docker/DockerGuideSteps'
import ExpansionPanel from '@/components/general/basic/ExpansionPanel'

export default {
  name: 'DockerGuide',
  components: {ExpansionPanel, DockerGuideSteps}
}
</script>

<style>

</style>
