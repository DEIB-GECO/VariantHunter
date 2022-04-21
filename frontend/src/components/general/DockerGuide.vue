<!--
  Component:    DockerGuide
  Description:  Guide to install and run the docker
-->

<template>
  <v-container class='mt-5'>
    <h3 id='docker_guide'>
      <v-icon left color='#000000DE' large>mdi-docker</v-icon>
      How to run the Docker
    </h3>
    <v-timeline v-if='!collapsed' dense align-top>

      <!------ PREREQUISITES ------>
      <v-timeline-item flat small color='red' class='mb-10' icon='mdi-information-variant'>
        <h4 class='red--text' id='prerequisites'>PREREQUISITES</h4>
        <ul class='red-list'>

          <li class='mb-2 mt-2'>
            Install <a href='https://www.docker.com/products/docker-desktop'>Docker Desktop</a>
          </li>

          <li>
            Download the metadata.tsv file
            <v-expansion-panels class='mt-3' accordion flat>

              <!---- GISAID GUIDE ---->
              <v-expansion-panel>
                <v-expansion-panel-header class='blue-grey lighten-5'><b>
                  <v-icon left color='black'>mdi-lifebuoy</v-icon>
                  How to download metadata.tsv from GISAID</b></v-expansion-panel-header>
                <v-expansion-panel-content class='blue-grey lighten-5'>
                  In order to download the metadata.tsv file from GISAID:
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
                <v-expansion-panel-header class='blue-grey lighten-5'><b>
                  <v-icon left color='black'>mdi-lifebuoy</v-icon>
                  How to download metadata.tsv from NEXTSTRAIN</b></v-expansion-panel-header>
                <v-expansion-panel-content class='blue-grey lighten-5'>
                  In order to download the metadata.tsv file from NEXTSTRAIN:
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
      <v-timeline-item flat small color='success' icon='mdi-play'>
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
        <v-simple-table class='mt-3 mb-4 alternate-rows table-with-borders'>
          <thead>
          <tr>
            <th class='text-left col-2'>Parameter name</th>
            <th class='text-left col-7'>Description</th>
            <th class='text-left col-3'>Required</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>FILE_PATH</td>
            <td>
              <p>Path to the <span class='monospaced'>.tsv</span> metadata file.</p>
              Example: <span class='pl-3 monospaced'>FILE_PATH=/Users/rossi/datasets/metadata.tsv</span>
            </td>
            <td><b>Required</b>.</td>
          </tr>
          <tr>
            <td>FILE_TYPE</td>
            <td>
              Type of the <span class='monospaced'>.tsv</span> metadata file. Currently supported:
              <ul>
                <li><span class='monospaced'>GISAID</span>: see <a href='#prerequisites'>prerequisites</a> for more
                  information
                </li>
                <li><span class='monospaced'>NEXTSTRAIN</span>: see <a href='#prerequisites'>prerequisites</a> for more
                  information
                </li>
              </ul>
              <p />
              Example: <span class='pl-3 monospaced'>FILE_TYPE=GISAID</span>
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>GISAID</span></td>
          </tr>
          <tr>
            <td>LOCATIONS</td>
            <td>
              <p>Comma separated list of country names whose sequence data is to be imported in the tool.<br />
                Use "<span class='monospaced'>All</span>" to import the entire dataset.</p>
              Example: <span class='pl-3 monospaced'>LOCATIONS="Italy"</span><br />
              Example: <span class='pl-3 monospaced'>LOCATIONS="Italy,Germany,Iran"</span>
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>"All"</span></td>
          </tr>
          <tr>
            <td>START_DATE</td>
            <td>
              <p>Start date to be considered when importing data. <br />
                Only the data in the period <span class='monospaced'>[START_DATE, END_DATE]</span> will be imported
                into the tool.</p>
              Example: <span class='pl-3 monospaced'>START_DATE=2021-12-01</span><br />
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>Beginning</span></td>
          </tr>
          <tr>
            <td>END_DATE</td>
            <td>
              <p>End date to be considered when importing data. <br />
                Only the data in the period <span class='monospaced'>[START_DATE, END_DATE]</span> will be imported
                into the tool.</p>
              Example: <span class='pl-3 monospaced'>END_DATE=2021-12-30</span><br />
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>End</span></td>
          </tr>

          <tr v-if='!showAllParams' class='expand-table'>
            <td colspan='3'>
              <v-chip small @click.native='showAllParams=true'>
                <v-icon small left color='black'>mdi-plus</v-icon>
                Show other optional advanced params
              </v-chip>
            </td>
          </tr>
          <tr v-if='showAllParams'>
            <td>RELOAD</td>
            <td>
              <p>Flag to drop the current database and reload the data from the <span class='monospaced'>.tsv</span>
                file. </p>
              Example: <span class='pl-3 monospaced'>RELOAD=true</span><br />
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>false</span></td>
          </tr>
          <tr v-if='showAllParams'>
            <td>PORT</td>
            <td>
              <p>The port to be used by the server</p>
              Example: <span class='pl-3 monospaced'>PORT=5001</span><br />
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>5000</span></td>
          </tr>
          <tr v-if='showAllParams'>
            <td>DB_PATH</td>
            <td>
              <p>Path to the <span class='monospaced'>varianthunter.db</span> database file or location where to
                generate it.</p>
              Usage:
              <ul>
                <li>export the database file</li>
                <li>use a database file resulting from a previous execution, avoiding
                  its regeneration starting from the <span class='monospaced'>.tsv</span> file.
                </li>
              </ul>
              <p />
              <p><u>Notice</u>: if a database already exists and <span class='monospaced'>FORCE=true</span> is not
                specified, then all the params are ignored and the specified database is loaded.
              </p>
              Example: <span class='pl-3 monospaced'>DB_PATH=/Users/rossi/save_db_here</span><br />
              Example: <span class='pl-3 monospaced'>DB_PATH=/Users/rossi/fetch_db_from_here</span><br />
            </td>
            <td><b>Optional</b>. <br />Default: <span class='monospaced'>internal path</span></td>
          </tr>
          </tbody>
        </v-simple-table>
        <div class='ml-5'>
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

      <v-timeline-item flat small color='success' icon='mdi-check'>
        Once the setup of the application is <b>completed</b> the log on the terminal shows the following message:<br />
        <span class='monospaced'> * STARTUP COMPLETED: The application is now accessible from your browser at
              http://0.0.0.0:&lt;PORT&gt;</span><br />
        Now the database has been loaded and the application is accessible from the browser.
        <v-alert class='mt-4' type='warning' outlined dense>
          Depending on the amount of data imported into the tool from the <span class='monospaced'>.tsv</span> file, the
          process may take some time and tens of GB. <b>It is strongly recommended to import only the data of interest
          for
          the analysis.</b>
        </v-alert>
      </v-timeline-item>

      <v-timeline-item flat small color='warning' icon='mdi-pause'>
        The process can be <b>stopped</b> on the terminal with <span class='monospaced'>CTRL+C</span>. <br />
        It can be restarted using the same or a new <span class='monospaced'>.tsv</span> file. In the latter case, the
        specification of <span class='monospaced'>RELOAD=true</span> is required to rerun the upload of the database.
      </v-timeline-item>
    </v-timeline>
    <v-container  class='pl-10 pr-10'>
      <v-btn v-if="collapsed" class='full-width-button black--text' @click.native='collapsed=false' color='#e0e0e0' large depressed outlined rounded>
        <v-icon left>mdi-plus</v-icon>
        <span class='black--text'>Show instructions</span>
      </v-btn>
      <v-btn v-else class='full-width-button black--text' @click.native='collapsed=true' color='#e0e0e0'  depressed outlined rounded>
        <v-icon left>mdi-minus</v-icon>
        <span class='black--text'>collapse</span>
      </v-btn>
    </v-container>
  </v-container>
</template>

<script>
import CodeBlock from '@/components/general/CodeBlock'

export default {
  name: 'DockerGuide',
  components: { CodeBlock },
  data () {
    return {
      /** Flag to show/hide the advanced otional params */
      showAllParams: false,

      /** Flag to show/hide the whole section*/
      collapsed: true
    }
  }
}
</script>

<style scoped>

/** Requirement red list */
ul.red-list li::marker {
  color: #F44336;
}

/* Table styling */
tr td:first-child, .monospaced {
  font-family: monospace !important;
}

.table-with-borders {
  border: thin solid rgba(0, 0, 0, 0.12) !important;
  border-radius: var(--border-radius) !important;
}

tbody tr td {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
  font-size: 14px !important;
}

tbody tr td:first-child {
  font-weight: bold;
}

.alternate-rows tr:nth-child(2n) {
  background: #f6f6f6;
}

.alternate-rows * :hover {
  background: #e0e0e0 !important;
}

.expand-table, .expand-table > *:hover {
  background: white !important;
}

.full-width-button {
  width: 100% !important;
}

</style>
