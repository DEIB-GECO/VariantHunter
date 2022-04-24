<!--
  Component:    DockerGuide
  Description:  Guide to install and run the docker
-->

<template>
  <v-container class='mt-5'>
    <div class='d-flex section-title flex-column flex-sm-row'>
      <h3 id='docker'>
        <v-icon left color='#000000DE' large>mdi-docker</v-icon>
        How to run the Docker
      </h3>
      <div v-if='!collapsed' class='pl-10 pr-10 collapse-button'>
        <v-chip @click='collapsed=true; showAllParams=false' color='#011936' depressed outlined>
          <v-icon small>mdi-close</v-icon>
          <span class='hidden-xs-only ml-2'>HIDE</span>
        </v-chip>
      </div>
    </div>
    <v-timeline v-if='!collapsed' dense align-top>

      <!------ PREREQUISITES ------>
      <v-timeline-item flat color='red' class='mb-10' icon='mdi-exclamation-thick'>
        <h4 class='red--text' id='prerequisites'>PREREQUISITES</h4>
        <ul class='red-list'>

          <li class='mb-2 mt-2'>
            <b>Install</b> the <a href='https://www.docker.com/products/docker-desktop'>Docker Desktop</a> app
          </li>

          <li>
            <b>Download</b> the <span class='monospaced'>metadata.tsv</span> file
            <v-expansion-panels class='mt-3' accordion flat>

              <!---- GISAID GUIDE ---->
              <v-expansion-panel>
                <v-expansion-panel-header class='blue-grey lighten-5'>
                  <v-col class='col-auto'><v-icon left color='black'>mdi-lifebuoy</v-icon></v-col>
                  <v-col>
                  How to download <span class='monospaced'>metadata.tsv</span> from GISAID
                  </v-col>
                </v-expansion-panel-header>
                <v-expansion-panel-content class='blue-grey lighten-5'>
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
                </v-expansion-panel-content>
              </v-expansion-panel>

              <!---- NEXTSTRAIN GUIDE ---->
              <v-expansion-panel>
                <v-expansion-panel-header class='blue-grey lighten-5'>
                  <v-col class='col-auto'><v-icon left color='black'>mdi-lifebuoy</v-icon></v-col>
                  <v-col>
                    How to download <span class='monospaced'>metadata.tsv</span> from NEXTSTRAIN
                  </v-col>
                </v-expansion-panel-header>
                <v-expansion-panel-content class='blue-grey lighten-5'>
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
                </v-expansion-panel-content>
              </v-expansion-panel>
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
      <v-timeline-item flat small color='success'>
        <b>Open</b> the terminal and move to the directory of the <span class='monospaced'>docker-compose.yml</span>
        file
      </v-timeline-item>
      <v-timeline-item flat small color='success'>
        <b>Run</b> the following command
        <CodeBlock code='docker pull gecopolimi/varianthunter' />
      </v-timeline-item>
      <v-timeline-item flat small color='success'>
        <b>Run</b> the following command
        <CodeBlock code='{parameters_list} docker-compose up' />
        <br />
        where {parameters_list} is a space-separated list of the following parameters:
        <DockerParamsTable v-model='showAllParams' />
        <div class='ml-5 examples'>
          <p>
            <i>Full example 1:</i><br />
            <CodeBlock code='FILE_PATH=/gisaid_metadata/metadata.tsv docker-compose up' />
          <p />
          <p>
            <i>Full example 2:</i><br />
            <CodeBlock code='FILE_PATH=/gisaid_metadata/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01
                docker-compose up' />
          </p>
          <p>
            <i>Full example 3:</i><br />
            <CodeBlock code='FILE_PATH=/nextstrain_metadata/metadata.tsv FILE_TYPE=NEXTSTRAIN docker-compose up' />
          <p />
        </div>

      </v-timeline-item>

      <!-- UP AND RUNNING -->
      <v-timeline-item flat color='success' icon='mdi-check-bold'>
        Once the setup is <b>completed</b> the log on the terminal shows the following message:<br />
        <span class='monospaced'> * STARTUP COMPLETED: The application is now accessible from your browser at
              http://0.0.0.0:&lt;PORT&gt;</span><br />
        Now the database has been loaded and the application is accessible from the browser.

        <!-- TIME/MEMORY ALERT -->
        <v-alert class='mt-4' type='warning' icon='mdi-exclamation-thick' outlined dense>
          Depending on the amount of data imported into the tool from the <span class='monospaced'>.tsv</span> file, the
          process may take some time and tens of GB. <b>It is strongly recommended to import only the data of interest
          for the analysis,</b> by specifying <span class='monospaced'>LOCATIONS</span>, <span class='monospaced'>
          START_DATE</span> and <span class='monospaced'>END_DATE</span>.
        </v-alert>

        <!-- MACOS ALERT -->
        <v-alert class='mt-4' type='error' icon='mdi-apple-finder' outlined dense>
          <b>When importing a considerable amount of data</b> (e.g. <span class='monospaced'>"All"</span> from
          <span class='monospaced'>Beginning</span> to <span class='monospaced'>End</span>) <b>while running macOS</b>
          it is strongly advised to follow
          <span class='fake-link' @click.self='showAlternativeGuide=true; showAllParams=false'>
            this alternative guide
          </span>
        </v-alert>
      </v-timeline-item>

      <!-- STOP STEP -->
      <v-timeline-item flat color='warning' icon='mdi-pause'>
        The process can be <b>stopped</b> on the terminal with <span class='monospaced'>CTRL+C</span>. <br />
        It can be restarted using the same or a new <span class='monospaced'>.tsv</span> file.

        <v-alert class='mt-5' color='deep-purple accent-4' icon='mdi-lifebuoy' outlined dense>
          Are you facing any problem?
          <span class='fake-link' @click.self='showTroubleshooting=true; showAllParams=false'>
            Troubleshooting
          </span>
          <DockerTroubleshooting v-model='showTroubleshooting'
                                 @showContacts='showContacts()'
                                 @openAltGuide='showAlternativeGuide=false; showAlternativeGuide=true'/>
        </v-alert>
      </v-timeline-item>
    </v-timeline>

    <v-container v-if='collapsed' class='pl-10 pr-10'>
      <v-btn class='full-width-button black--text' @click.native='collapsed=false' color='#e0e0e0'
             large depressed outlined rounded>
        <v-icon left>mdi-plus</v-icon>
        <span class='black--text'>Show instructions</span>
      </v-btn>
    </v-container>

    <!---- ALTERNATIVE GUIDE ---->
    <v-dialog v-model='showAlternativeGuide' max-width='1100' transition='dialog-bottom-transition'>
      <v-card>
        <!-- Dialog title -->
        <v-toolbar :color='primary_color' class='dialog-title' dark flat>
          <v-icon left large>mdi-apple-finder</v-icon>
          Alternative guide for macOS
        </v-toolbar>

        <!-- Dialog content -->
        <v-card-text class='text-s-center black--text dialog-text underlined-links'>
          <slot>
            <p>
              Due to how Docker works in the macOS version, you may notice an <b class='red--text'>unusual storage
              occupation</b> when loading the database. Indeed, Docker does not automatically resize the
              volumes by releasing free space to the host user. <b class='red--text'>This could cause the procedure to
              fail when dealing with large amount of data, if there is not enough space available.</b>
            </p>
            <p>
              To overcome this issue, please consider the following changes to the standard procedure:
            </p>
            <v-timeline dense align-top>
              <!------ STEPS ------>
              <v-timeline-item flat color='grey' icon='mdi-play'>
                <b>Open</b> the Docker Desktop app
              </v-timeline-item>
              <v-timeline-item flat small color='grey'>
                <b>Download</b> the <span class='monospaced'>docker-compose.yml</span> file from <a
                href='https://github.com/DEIB-GECO/VariantHunter/blob/master/docker-compose.yml' target='_blank'> this
                link</a>
              </v-timeline-item>
              <v-timeline-item flat small color='success'>
                <b>Download</b> the <span class='monospaced'>launcher.sh</span> file from <a
                href='https://github.com/DEIB-GECO/VariantHunter/blob/master/launcher.sh' target='_blank'> this
                link</a> and move it into the same folder of the <span class='monospaced'>docker-compose.yml</span> file
              </v-timeline-item>
              <v-timeline-item flat small color='grey'>
                <b>Open</b> the terminal and move to the directory of the <span
                class='monospaced'>docker-compose.yml</span>
                file
              </v-timeline-item>
              <v-timeline-item flat small color='success'>
                <b>Run</b> the following command
                <CodeBlock code='/bin/zsh ./launcher.sh {parameters_list}' />
                where {parameters_list} is the space-separated list of the parameters
                <div class='ml-5 examples'>
                  <p>
                    <i>Full example 1:</i><br />
                    <CodeBlock code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv' />
                  <p />
                  <p>
                    <i>Full example 2:</i><br />
                    <CodeBlock
                      code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01' />
                  </p>
                  <p>
                    <i>Full example 3:</i><br />
                    <CodeBlock
                      code='/bin/zsh ./launcher.sh FILE_PATH=/nextstrain_metadata/metadata.tsv FILE_TYPE=NEXTSTRAIN' />
                  <p />
                </div>

              </v-timeline-item>

              <!-- UP AND RUNNING -->
              <v-timeline-item flat color='grey' icon='mdi-check-bold'>
                Once the setup is <b>completed</b> the log on the terminal shows the following
                message:<br />
                <span class='monospaced'> * STARTUP COMPLETED: The application is now accessible from your browser at
              http://0.0.0.0:&lt;PORT&gt;</span><br />
                Now the database has been loaded and the application is accessible from the browser.
              </v-timeline-item>

              <!-- STOP STEP -->
              <v-timeline-item flat color='grey' icon='mdi-pause'>
                The process can be <b>stopped</b> on the terminal with <span class='monospaced'>CTRL+C</span> and
                following the instruction provided from the terminal. <br />
                It can be restarted using the same or a new <span class='monospaced'>.tsv</span> file.
              </v-timeline-item>
            </v-timeline>
          </slot>
        </v-card-text>

        <!-- Dialog actions -->
        <v-card-actions class='justify-end'>
          <v-btn text @click='showAlternativeGuide = false'>
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import CodeBlock from '@/components/general/CodeBlock'
import { mapState } from 'vuex'
import DockerParamsTable from '@/components/general/guides/docker/DockerParamsTable'
import DockerTroubleshooting from '@/components/general/guides/docker/DockerTroubleshooting'

export default {
  name: 'DockerGuide',
  components: { DockerTroubleshooting, DockerParamsTable, CodeBlock },
  data () {
    return {
      /** Flag to show/hide the advanced optional params */
      showAllParams: false,

      /** Flag to show/hide the alternative guide */
      showAlternativeGuide: false,

      /** Flag to show/hide the troubleshooting guide */
      showTroubleshooting: false,

      /** Flag to show/hide the whole section*/
      collapsed: true
    }
  },
  computed: {
    ...mapState(['primary_color'])
  },
  methods: {
    /** Go to the contacts section by hiding all the dialogs */
    showContacts () {
      this.showAlternativeGuide = false
      this.showTroubleshooting = false
      document.getElementById('contributors').scrollIntoView()
    }
  }

}
</script>

<style scoped>

/** Requirement red list */
ul.red-list li::marker {
  color: #F44336;
}

/** Reduce emphasis of code examples*/
.examples, .examples * {
  font-size: 14px !important;
}

/** Styling for collapse button*/
.section-title {
  justify-content: space-between;
}

.collapse-button * {
  float: right;
}
</style>
<style>

/** Fake links styling */
.fake-link {
  text-decoration: underline;
  cursor: pointer;
  font-weight: 500;
}

</style>
