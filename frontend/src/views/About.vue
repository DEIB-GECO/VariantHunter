<!--
  View:         About
  Description:  Component for the about section.
-->

<template>
  <v-container>

    <!-- Website title -->
    <v-row class='justify-center mt-5'>
      <v-col cols='col-xs-12 col-sm-3 col-lg-2'>
        <div class='huge-title'>
          <div class='huge-logo hidden-xs-only'>
            <v-img :src='websiteLogo' contain height='150px' width='150px' />
          </div>
          <v-img :src='websiteLogo' class='hidden-sm-and-up' contain height='80px' width='80px' />
        </div>
      </v-col>
      <v-col cols='col-xs-12 col-sm-5 col-lg-3'>
        <div class='site-title huge-site-title'>
          <span class='emphasis'>Variant</span><br />
          <span>Hunter</span>
        </div>
      </v-col>
    </v-row>

    <!-- Buttons -->
    <v-row class='justify-center mb-10'>
      <v-col cols='col-xs-12 col-sm-4 col-lg-3 d-flex justify-center'>
        <router-link to='/variant_hunter'>
          <v-btn class='' color='#011936' depressed outlined rounded>
            <v-icon left>mdi-virus-outline</v-icon>
            Go to the tool
          </v-btn>
        </router-link>
      </v-col>
      <v-col cols='col-xs-12 col-sm-4 col-lg-3 d-flex justify-center'>
        <a href='https://github.com/DEIB-GECO/VariantHunter' target='_blank'>
          <v-btn class='' color='#347D39' depressed outlined rounded>
            <v-icon left>mdi-github</v-icon>
            View on Github
          </v-btn>
        </a>
      </v-col>
    </v-row>

    <!-- Docker info -->
    <v-row class='with-separator'>
      <v-container class='pa-10 pb-0 mt-5'>
        <h3>
          <v-icon left color='#000000DE' large>mdi-docker</v-icon>
          How to run the Docker
        </h3>
        <v-timeline dense align-top>
          <v-timeline-item flat small color='#000000DE'>
            Open the terminal and run
            <CodeBlock>docker pull gecopolimi/varianthunter</CodeBlock>
          </v-timeline-item>
          <v-timeline-item flat small color='#000000DE'>
            Run the following command
            <CodeBlock><i>{parameters_list}</i> &nbsp;&nbsp;docker-compose up</CodeBlock>
            <br />
            where {parameters_list} is a space-separated list of the following parameters:
            <v-simple-table class='mt-3 mb-4'>
              <thead>
              <tr>
                <th class='text-left'>Parameter name</th>
                <th class='text-left'>Description</th>
                <th class='text-left'>Required</th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td>FILE_PATH</td>
                <td>
                  <p>Path to the folder containing the <span class='monospaced'>.tsv</span> metadata file.</p>
                  Example: <span class='pl-3 monospaced'>FILE_PATH=/Users/rossi/datasets</span>
                </td>
                <td>Required</td>
              </tr>
              <tr>
                <td>FILE_NAME</td>
                <td>
                  <p>Name of the <span class='monospaced'>.tsv</span> metadata file (extension included).</p>
                  Example: <span class='pl-3 monospaced'>FILE_NAME=metadata.tsv</span>
                </td>
                <td>Required</td>
              </tr>
              <tr>
                <td>FILE_TYPE</td>
                <td>
                  Type of the <span class='monospaced'>.tsv</span> metadata file. Currently supported:
                  <ul>
                    <li><span class='monospaced'>GISAID</span> :
                      <a href='https://www.epicov.org/epi3/frontend' target='_blank'>more info</a></li>
                    <li><span class='monospaced'>NEXTSTRAIN</span> :
                      <a href='https://nextstrain.org/ncov/open/global' target='_blank'>more info</a></li>
                  </ul>
                  <p />
                  Example: <span class='pl-3 monospaced'>FILE_TYPE=GISAID</span>
                </td>
                <td>Optional. <br />Default: <span class='monospaced'>GISAID</span></td>
              </tr>
              <tr>
                <td>LOCATIONS</td>
                <td>
                  <p>Comma separated list of country names whose sequence data is to be imported in the tool.<br />
                    Use "<span class='monospaced'>All</span>" to import the entire dataset.</p>
                  Example: <span class='pl-3 monospaced'>LOCATIONS="Italy"</span><br />
                  Example: <span class='pl-3 monospaced'>LOCATIONS="Italy,Germany,Iran"</span>
                </td>
                <td>Optional <br />Default: <span class='monospaced'>"All"</span></td>
              </tr>
              <tr>
                <td>PORT</td>
                <td>
                  <p>The port to be used by the server</p>
                  Example: <span class='pl-3 monospaced'>PORT=5001</span><br />
                </td>
                <td>Optional <br />Default: <span class='monospaced'>5000</span></td>
              </tr>
              <tr>
                <td>START_DATE</td>
                <td>
                  <p>Start date to be considered when importing data. <br />
                    Only the data in the period <span class='monospaced'>[START_DATE, END_DATE]</span> will be imported
                    into the tool.</p>
                  Example: <span class='pl-3 monospaced'>START_DATE=01-12-2021</span><br />
                </td>
                <td>Optional <br />Default: <span class='monospaced'>Beginning</span></td>
              </tr>
              <tr>
                <td>END_DATE</td>
                <td>
                  <p>End date to be considered when importing data. <br />
                    Only the data in the period <span class='monospaced'>[START_DATE, END_DATE]</span> will be imported
                    into the tool.</p>
                  Example: <span class='pl-3 monospaced'>START_DATE=01-12-2021</span><br />
                </td>
                <td>Optional <br />Default: <span class='monospaced'>End</span></td>
              </tr>
              </tbody>
            </v-simple-table>

            <p>
              Full example 1:<br/>
              <CodeBlock>FILE_PATH=/metadata/ FILE_NAME=metadata.tsv docker-compose up</CodeBlock>
            <p />
            <p>
              Full example 2:<br/>
              <CodeBlock>FILE_PATH=/metadata/ FILE_NAME=metadata.tsv LOCATION="Italy" START_DATE=01-12-2021 docker-compose up</CodeBlock>
            </p>

          </v-timeline-item>

        </v-timeline>
      </v-container>
    </v-row>

    <!-- Behind the tool -->
    <v-row>
      <v-container class='pa-10'>

        <h3>
          <v-icon left color='#000000DE' large>mdi-account-supervisor</v-icon>
          Contributors
        </h3>

        <v-timeline dense class='contributors-list'>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='defaultPic' alt='Picture of Anna Bernasconi'>
              </v-avatar>
            </template>
            Anna Bernasconi
            <span class='associate-label'>Politecnico di Milano</span>
          </v-timeline-item>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='defaultPic' alt='Picture of Stefano Ceri'>
              </v-avatar>
            </template>
            Stefano Ceri
            <span class='associate-label'>Politecnico di Milano</span>
          </v-timeline-item>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='defaultPic' alt='Picture of Matteo Chiara'>
              </v-avatar>
            </template>
            Matteo Chiara
            <span class='associate-label'>Università degli Studi di Milano Statale</span>
          </v-timeline-item>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='defaultPic' alt='Picture of Arif Canakoglu'>
              </v-avatar>
            </template>
            Arif Canakoglu
            <span class='associate-label'>Policlinico di Milano</span>
          </v-timeline-item>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='defaultPic' alt='Picture of Luca Minotti'>
              </v-avatar>
            </template>
            Luca Minotti
            <span class='associate-label'>Politecnico di Milano</span>
          </v-timeline-item>

          <v-timeline-item flat>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='pinoliPic' alt='Picture of Pietro Pinoli'>
              </v-avatar>
            </template>
            Pietro Pinoli
            <span class='associate-label'>Politecnico di Milano</span>
          </v-timeline-item>

        </v-timeline>
      </v-container>
    </v-row>

  </v-container>

</template>

<script>
import { mapState } from 'vuex'
import CodeBlock from '@/components/general/CodeBlock'

export default {
  name: 'About',
  components: { CodeBlock },
  data () {
    return {
      /** VariantHunter logo */
      websiteLogo: require('../assets/virusurf_logo.png'),

      /** Contributors icon */
      defaultPic: require('../assets/contributors/person.png'),
      pinoliPic: require('../assets/contributors/pinoli.png')
    }
  },
  computed: {
    ...mapState(['primary_color', 'tertiary_color_dark', 'tertiary_color_light'])
  }
}
</script>

<style scoped>

.huge-title {
  margin: auto;
  justify-content: center;
  display: flex;
}

.huge-logo {
  float: right !important;
}

.huge-site-title {
  text-align: center;
  color: var(--primary-color);
  font-size: 67px;
  line-height: 65px;
}

h3 {
  font-size: 20px;
  font-weight: 900;
  text-transform: uppercase;
}

.theme--light.v-timeline::before {
  background: #000000DE;
  border-radius: 3px;
}

.with-separator {
  border-top: 2px solid #000000DE;
}

.associate-label {
  display: block;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: normal;
}

.contributors-list {
  font-size: initial;
  font-weight: 600;
}

tr td:first-child, .monospaced {
  font-family: monospace !important;
}

tbody tr td {
  padding-top: 10px !important;
  padding-bottom: 10px !important;
  font-size: 14px !important;
}

</style>
