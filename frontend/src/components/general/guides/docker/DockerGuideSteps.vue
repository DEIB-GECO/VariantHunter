<!--
  Component:    DockerGuideSteps
  Description:  Steps of the docker guide

  Props:
  └── macGuide: Mac guide flag: true iff the guide is for macOS

-->

<template>
  <v-timeline dense align-top class='pr-0 mr-0 pl-0 ml-0'>

    <v-timeline-item v-if='macGuide' flat color='info' class='mb-5' icon='mdi-bug-outline'>
      <p>
        Due to the fact that Docker for macOS does not automatically resize volumes
        during processing (releasing free space to the host user),
        <b class='info--text'> additional steps are required to prevent unusual storage occupation</b>
        during database loading (which could cause failure if there is little space available). <br />
        Please proceed according to the following steps.
      </p>
    </v-timeline-item>

    <!------ PREREQUISITES ------>
    <v-timeline-item flat color='red' class='mb-10' icon='mdi-exclamation-thick'>
      <h4 class='red--text' id='prerequisites'>PREREQUISITES</h4>
      <ul class='red-list aligned-list'>

        <li class='mb-2 mt-2'>
          <b>Install</b> the <a href='https://www.docker.com/products/docker-desktop'>Docker Desktop</a> app
        </li>

        <li>
          <b>Download</b> the <span class='monospaced'>metadata.tsv</span> file
          <v-expansion-panels class='mt-3' accordion flat>

            <!---- GISAID GUIDE ---->
            <ExpansionPanel>
              <template v-slot:icons>
                <v-icon left color='black'>mdi-lifebuoy</v-icon>
              </template>
              <template v-slot:title>
                How to download <span class='monospaced'>metadata.tsv</span> from GISAID
              </template>
              <template v-slot:default>
                In order to download the <span class='monospaced'>metadata.tsv</span> file from GISAID:
                <ul class='red-list'>
                  <li class='mb-2 mt-2'>
                    Login into your <a href='https://www.epicov.org/epi3/frontend' target='_blank'>GISAID</a> account
                  </li>
                  <li class='mb-2 mt-2'>
                    In the <i>''EpiCoV''</i> toolbar, select <i>''Downloads''</i>
                  </li>
                  <li class='mb-2 mt-2'>
                    From the <i>''Download packages''</i> section, select the <i>''metadata''</i> option
                  </li>
                  <li class='mb-2 mt-2'>
                    Once downloaded, unzip the archive
                  </li>
                </ul>
              </template>
            </ExpansionPanel>

            <!---- NEXTSTRAIN GUIDE ---->
            <ExpansionPanel>
              <template v-slot:icons>
                <v-icon left color='black'>mdi-lifebuoy</v-icon>
              </template>
              <template v-slot:title>
                How to download <span class='monospaced'>metadata.tsv</span> from NEXTSTRAIN
              </template>
              <template v-slot:default>
                In order to download the <span class='monospaced'>metadata.tsv</span> file from NEXTSTRAIN:
                <ul class='red-list'>
                  <li class='mb-2 mt-2'>
                    Visit <a href='https://nextstrain.org/ncov/open/global' target='_blank'>this link</a>
                  </li>
                  <li class='mb-2 mt-2'>
                    In the <i>''All sequences and metadata''</i> section, download the <span class='monospaced'>metadata.tsv.gz</span>
                    file
                  </li>
                  <li class='mb-2 mt-2'>
                    Once downloaded, unzip the archive
                  </li>
                </ul>
              </template>
            </ExpansionPanel>
          </v-expansion-panels>
        </li>
      </ul>
    </v-timeline-item>

    <!------ STEPS ------>
    <v-timeline-item flat color='success' icon='mdi-play'>
      <b>Open</b> the Docker Desktop app
    </v-timeline-item>

    <v-timeline-item flat small color='success'>
      <b>Download</b> the <span class='monospaced'>docker-compose.yml</span> file from <a
      href='https://github.com/DEIB-GECO/VariantHunter/blob/master/docker-compose.yml' target='_blank'> this link</a>
    </v-timeline-item>

    <v-timeline-item v-if='macGuide' flat small color='success'>
      <b>Download</b> the <span class='monospaced'>launcher.sh</span> file from <a
      href='https://github.com/DEIB-GECO/VariantHunter/blob/master/launcher.sh' target='_blank'> this
      link</a> and move it into the same folder of the <span class='monospaced'>docker-compose.yml</span> file
    </v-timeline-item>

    <v-timeline-item flat small color='success'>
      <b>Open</b> the terminal and move to the directory of the <span class='monospaced'>docker-compose.yml</span>
      file
    </v-timeline-item>

    <v-timeline-item v-if='!macGuide' flat small color='success'>
      <b>Run</b> the following command
      <CodeBlock code='docker pull gecopolimi/varianthunter' />
    </v-timeline-item>

    <v-timeline-item flat small color='success'>
      <b>Run</b> the following command
      <CodeBlock v-if='!macGuide' code='{parameters_list} docker-compose up' />
      <CodeBlock v-else code='/bin/zsh ./launcher.sh {parameters_list}' />
      <br />
      where {parameters_list} is a space-separated list of the following parameters:
      <DockerParamsTable v-model='showAllParams' />
      <div class='ml-0 ml-sm-5 examples'>
        <p>
          <i>Full example 1 &nbsp;&nbsp; [ generation from .tsv file ]:</i><br />
          <CodeBlock v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv docker-compose up'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file'
          />
          <CodeBlock v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file'
          />
        <p />
        <p>
          <i>Full example 2 &nbsp;&nbsp; [ generation from .tsv file with filters ]:</i><br />
          <CodeBlock v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01 docker-compose up'
                     hover='This generates a new database starting from the sequences of the <span class="monospaced">metadata.tsv</span> file collected starting <b>from 2021-12-01 in Italy</b>'
          />
          <CodeBlock v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01'
                     hover='This generates a new database starting from the sequences of the <span class="monospaced">metadata.tsv</span> file collected starting <b>from 2021-12-01 in Italy</b>'
          />

        </p>
        <p>
          <i>Full example 3 &nbsp;&nbsp; [ importing an existing database ]:</i><br />
          <CodeBlock v-if='!macGuide'
                     code='DB_PATH=./fetch_existing_db_from_here docker-compose up'
                     hover='This loads the <span class="monospaced">varianthunter.db</span> database file located in the specified folder</b>'
          />
          <CodeBlock v-else
                     code='/bin/zsh ./launcher.sh DB_PATH=./fetch_existing_db_from_here'
                     hover='This loads the <span class="monospaced">varianthunter.db</span> database file located in the specified folder</b>'
          />

        <p />
        <p>
          <i>Full example 4 &nbsp;&nbsp; [ generation from .tsv file + export ]:</i><br />
          <CodeBlock v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv DB_PATH=./save_db_here docker-compose up'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file, <b>exporting it into the save_db_here folder</b> for later usage'
          />
          <CodeBlock v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid/metadata.tsv DB_PATH=./save_db_here'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file, <b>exporting it into the save_db_here folder</b> for later usage'
          />

        </p>
      </div>

      <!-- TIME/MEMORY ALERT -->
      <v-alert class='mt-4' type='warning' icon='mdi-exclamation-thick' outlined dense>
        Depending on the amount of data imported into the tool from the <span class='monospaced'>.tsv</span> file, the
        process may take some time and tens of GB (10M sequences may require even 30 GB to be processed). <b>It is
        strongly recommended to import only the data of interest
        for the analysis,</b> by specifying <span class='monospaced'>LOCATIONS</span>, <span class='monospaced'>
          START_DATE</span> and <span class='monospaced'>END_DATE</span>.
      </v-alert>
    </v-timeline-item>

    <!-- UP AND RUNNING -->
    <v-timeline-item flat color='success' icon='mdi-check-bold'>
      Once the setup is <b>completed</b> the log on the terminal shows the following message:<br />
      <span class='monospaced'> * STARTUP COMPLETED: The application is now accessible from your browser at
              http://0.0.0.0:&lt;PORT&gt;</span><br />
      Now the database has been loaded and the application is accessible from the browser.
    </v-timeline-item>

    <!-- STOP STEP -->
    <v-timeline-item flat color='warning' icon='mdi-pause'>
      The process can be <b>stopped</b> on the terminal with <span class='monospaced'>CTRL+C</span>
      <span v-if='macGuide'> and following the instruction provided from the terminal</span>. <br />
      It can be restarted using the same or a new <span class='monospaced'>.tsv</span> file.

      <v-alert class='mt-5' color='deep-purple accent-4' icon='mdi-lifebuoy' outlined dense>
        Are you facing any problem?
        <span class='fake-link' @click.self='showTroubleshooting=true; showAllParams=false'>
            Troubleshooting
          </span>
        <DockerTroubleshooting v-model='showTroubleshooting' />
      </v-alert>
    </v-timeline-item>

  </v-timeline>
</template>

<script>
import CodeBlock from '@/components/general/CodeBlock'
import DockerTroubleshooting from '@/components/general/guides/docker/DockerTroubleshooting'
import DockerParamsTable from '@/components/general/guides/docker/DockerParamsTable'
import ExpansionPanel from '@/components/general/ExpansionPanel'

export default {
  name: 'DockerGuideSteps',
  components: { ExpansionPanel, DockerParamsTable, CodeBlock, DockerTroubleshooting },
  props: {
    /** Mac guide flag: true iff the guide is for macOS */
    macGuide: Boolean
  },
  data () {
    return {
      /** Flag to show/hide the advanced optional params */
      showAllParams: false,

      /** Flag to show/hide the troubleshooting guide */
      showTroubleshooting: false
    }
  }
}
</script>

<style scoped>

/** Requirements red list */
ul.red-list li::marker {
  color: #F44336;
}

ul.aligned-list {
  padding-left: 0 !important;
}

/** Reduce emphasis of code examples*/
.examples, .examples * {
  font-size: 14px !important;
}

</style>
