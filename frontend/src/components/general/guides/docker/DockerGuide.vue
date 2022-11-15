<!--
  Component:    DockerGuide
  Description:  Container for the guides to install and run the docker
-->

<template>
  <v-container class='ml-0 ml-sm-auto mr-0 mr-sm-auto mt-5'>
    <h3 id='docker'>
      <v-icon left large>mdi-docker</v-icon>
      How to run the Docker
    </h3>
    <v-container class='pl-0 pl-sm-10 pr-0 pr-sm-10 pb-5'>

      <v-expansion-panels class='mt-3' flat>

        <!-- WINDOWS LINUX GUIDE -->
        <ExpansionPanel double-icon>
          <template v-slot:icons>
            <v-icon >mdi-microsoft</v-icon>
            <v-icon >mdi-slash-forward</v-icon>
            <v-icon left color='#000000DE'>mdi-penguin</v-icon>
          </template>
          <template v-slot:title>
            <span class='hidden-xs-only'>Instructions for </span> <b>Windows / Linux</b>
          </template>
          <template v-slot:default>
            <DockerGuideSteps />
          </template>
        </ExpansionPanel>

        <!-- MACOS GUIDE -->
        <ExpansionPanel double-icon>
          <template v-slot:icons>
            <v-icon left color='#000000DE'>mdi-apple</v-icon>
          </template>
          <template v-slot:title>
            <span class='hidden-xs-only'>Instructions for </span> <b>MacOS</b>
          </template>
          <template v-slot:default>
            <DockerGuideSteps mac-guide />
          </template>
        </ExpansionPanel>

      </v-expansion-panels>
    </v-container>
  </v-container>
</template>

<script>
import DockerGuideSteps from '@/components/general/guides/docker/DockerGuideSteps'
import ExpansionPanel from '@/components/general/ExpansionPanel'

export default {
  name: 'DockerGuide',
  components: { ExpansionPanel, DockerGuideSteps }
}
</script>

<style>

</style>
