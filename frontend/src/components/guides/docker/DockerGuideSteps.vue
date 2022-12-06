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
    <v-timeline-item flat color='error' class='mb-10' icon='mdi-exclamation-thick'>
      <h4 class='error--text' id='prerequisites'>PREREQUISITES</h4>
      <ul class='red-list aligned-list'>

        <li class='mb-2 mt-2'>
          <b>Install</b> the <a href='https://www.docker.com/products/docker-desktop'>Docker Desktop</a> app
        </li>

        <li>
          <b>Download</b> the <span class='monospaced'>metadata.tsv</span> file
          <v-expansion-panels class='mt-3' accordion flat>

            <!---- GISAID GUIDE ---->
            <expansion-panel>
              <template v-slot:icons>
                <v-icon left color='text_var1'>mdi-lifebuoy</v-icon>
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
            </expansion-panel>

            <!---- NEXTSTRAIN GUIDE ---->
            <expansion-panel>
              <template v-slot:icons>
                <v-icon left color='text_var1'>mdi-lifebuoy</v-icon>
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
            </expansion-panel>
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
      href='https://github.com/DEIB-GECO/VariantHunter/blob/master/docker-compose.yml' target='_blank'> this</a> link
      <br />
      <v-tooltip bottom color='text_var1' max-width='400'>
        <template v-slot:activator='{ on, attrs }'>
        <span v-bind='attrs'
              v-on='on'>
          <a class='direct-link' target='_blank'
             href='https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/DEIB-GECO/VariantHunter/blob/master/docker-compose.yml'>
            <v-icon left x-small color='secondary'>mdi-monitor-arrow-down-variant</v-icon>DIRECT DOWNLOAD
          </a>
        </span>
        </template>
        <span>
        Download docker-compose.yml file as zip arhcive. <br />
        If you use this link, then you also <b>need to unzip the archive</b>.
        </span>
      </v-tooltip>
    </v-timeline-item>

    <v-timeline-item v-if='macGuide' flat small color='success'>
      <b>Download</b> the <span class='monospaced'>launcher.sh</span> file from <a
      href='https://github.com/DEIB-GECO/VariantHunter/blob/master/launcher.sh' target='_blank'> this</a>
      link and move it into the same folder of the <span class='monospaced'>docker-compose.yml</span> file<br />
      <v-tooltip bottom color='text_var1' max-width='400'>
        <template v-slot:activator='{ on, attrs }'>
        <span v-bind='attrs'
              v-on='on'>
          <a class='direct-link' target='_blank'
             href='https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/DEIB-GECO/VariantHunter/blob/master/launcher.sh'>
            <v-icon left x-small color='secondary'>mdi-monitor-arrow-down-variant</v-icon>DIRECT DOWNLOAD
          </a>
        </span>
        </template>
        <span>
        Download launcher.sh file as zip arhcive. <br />
        If you use this link, then you also <b>need to unzip the archive</b>.
      </span>
      </v-tooltip>
    </v-timeline-item>

    <v-timeline-item flat small color='success'>
      <b>Open</b> the terminal and move to the directory of the <span class='monospaced'>docker-compose.yml</span>
      file
    </v-timeline-item>

    <v-timeline-item v-if='!macGuide' flat small color='success'>
      <b>Run</b> the following command
      <code-block code='docker pull gecopolimi/varianthunter' />
    </v-timeline-item>

    <v-timeline-item flat small color='success'>
      <b>Run</b> the following command
      <code-block v-if='!macGuide' code='{parameters_list} docker-compose up' />
      <code-block v-else code='/bin/zsh ./launcher.sh {parameters_list}' />
      <br />
      where {parameters_list} is a space-separated list of the following parameters:
      <docker-params-table v-model='showAllParams' />
      <div class='ml-0 ml-sm-5 examples'>
        <p>
          <i>Full example 1 &nbsp;&nbsp; [ generation from .tsv file ]:</i><br />
          <code-block v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv docker-compose up'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file'
          />
          <code-block v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file'
          />
        <p />
        <p>
          <i>Full example 2 &nbsp;&nbsp; [ generation from .tsv file with filters ]:</i><br />
          <code-block v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01 docker-compose up'
                     hover='This generates a new database starting from the sequences of the <span class="monospaced">metadata.tsv</span> file collected starting <b>from 2021-12-01 in Italy</b>'
          />
          <code-block v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid_metadata/metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01'
                     hover='This generates a new database starting from the sequences of the <span class="monospaced">metadata.tsv</span> file collected starting <b>from 2021-12-01 in Italy</b>'
          />

        </p>
        <p>
          <i>Full example 3 &nbsp;&nbsp; [ importing an existing database ]:</i><br />
          <code-block v-if='!macGuide'
                     code='DB_PATH=./fetch_existing_db_from_here docker-compose up'
                     hover='This loads the <span class="monospaced">varianthunter.db</span> database file located in the specified folder</b>'
          />
          <code-block v-else
                     code='/bin/zsh ./launcher.sh DB_PATH=./fetch_existing_db_from_here'
                     hover='This loads the <span class="monospaced">varianthunter.db</span> database file located in the specified folder</b>'
          />

        <p />
        <p>
          <i>Full example 4 &nbsp;&nbsp; [ generation from .tsv file + export ]:</i><br />
          <code-block v-if='!macGuide'
                     code='FILE_PATH=/gisaid/metadata.tsv DB_PATH=./save_db_here docker-compose up'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file, <b>exporting it into the save_db_here folder</b> for later usage'
          />
          <code-block v-else
                     code='/bin/zsh ./launcher.sh FILE_PATH=/gisaid/metadata.tsv DB_PATH=./save_db_here'
                     hover='This generates a new database starting from <b>all</b> the sequences of the <span class="monospaced">metadata.tsv</span> file, <b>exporting it into the save_db_here folder</b> for later usage'
          />

        </p>
      </div>

      <!-- TIME/MEMORY ALERT -->
      <v-alert class='mt-4' type='warning' icon='mdi-exclamation-thick' outlined dense>
        <p>
          <b>It is strongly recommended to import into the tool only the data of
            interest for the intended analysis</b> (by specifying
          <span class='monospaced'>LOCATIONS</span>,
          <span class='monospaced'>START_DATE</span> and
          <span class='monospaced'>END_DATE</span>),
          as the database generation may require <u>significant time and storage resources</u>.
        </p>

        <i>Consider that, on a standard machine (macOS, 4 cores, 16GB RAM), generating a database starting from:</i>
        <ul>
          <li>
            <i>~10M sequences (size of GISAID <span class='monospaced'>metadata.tsv</span>
              as of April 2022) may require ~30GB (during processing) and ~2 hrs.
              In this case, after the processing, the Docker container requires ~8GB;</i>
          </li>
          <li>
            <i>~1M sequences may require ~5GB (during processing) and ~30 min.</i>
          </li>
        </ul>
      </v-alert>
      <v-alert class='mt-4' type='warning' icon='mdi-exclamation-thick' outlined dense>
        <p>
          <b>It is also suggested to always export the database file</b> by specifying the <span class='monospaced'>DB_PATH</span>
          parameter, so that the Docker container can be restarted instantaneously in the next sessions
          (no need to regenerate the database from the <span class='monospaced'>.tsv</span> file).</p>
        <p>
          This operation may slow down the procedure <i>(order of 3 hrs on the above configuration
          involving ~10M sequences)</i>.
          For complex analyses, it is suggested to generate the database when the machine is not in use
          (e.g. overnight).
        </p>
      </v-alert>
    </v-timeline-item>

    <!-- UP AND RUNNING -->
    <v-timeline-item flat color='success' icon='mdi-check-bold'>
      Once the setup is <b>completed</b> the log on the terminal shows the following message:<br />
      <span class='monospaced'> * STARTUP COMPLETED: The application is now accessible from your browser at
              http://localhost:&lt;PORT&gt;</span><br />
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
        <docker-troubleshooting v-model='showTroubleshooting' />
      </v-alert>
    </v-timeline-item>

  </v-timeline>
</template>

<script>
import CodeBlock from '@/components/general/basic/CodeBlock'
import DockerTroubleshooting from '@/components/guides/docker/DockerTroubleshooting'
import DockerParamsTable from '@/components/guides/docker/DockerParamsTable'
import ExpansionPanel from '@/components/general/basic/ExpansionPanel'

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
  color: var(--v-error-base);
}

ul.aligned-list {
  padding-left: 0 !important;
}

/** Reduce emphasis of code examples*/
.examples, .examples * {
  font-size: 14px !important;
}

.direct-link {
  font-size: 12px !important;
  border: 1px solid;
  padding: 0 10px;
  cursor: copy !important;
  border-radius: 20px;
  break-inside: avoid !important;
  display: inline-block;
}

</style>
