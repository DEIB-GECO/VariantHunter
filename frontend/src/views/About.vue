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
                  Example: <span class='pl-3 monospaced'>START_DATE=2021-12-01</span><br />
                </td>
                <td>Optional <br />Default: <span class='monospaced'>Beginning</span></td>
              </tr>
              <tr>
                <td>END_DATE</td>
                <td>
                  <p>End date to be considered when importing data. <br />
                    Only the data in the period <span class='monospaced'>[START_DATE, END_DATE]</span> will be imported
                    into the tool.</p>
                  Example: <span class='pl-3 monospaced'>START_DATE=2021-12-30</span><br />
                </td>
                <td>Optional <br />Default: <span class='monospaced'>End</span></td>
              </tr>
              </tbody>
            </v-simple-table>

            <p>
              Full example 1:<br />
              <CodeBlock>FILE_PATH=/metadata/ FILE_NAME=metadata.tsv docker-compose up</CodeBlock>
            <p />
            <p>
              Full example 2:<br />
              <CodeBlock>FILE_PATH=/metadata/ FILE_NAME=metadata.tsv LOCATIONS="Italy" START_DATE=2021-12-01
                docker-compose up
              </CodeBlock>
            </p>

          </v-timeline-item>

        </v-timeline>
      </v-container>
    </v-row>

    <!-- Contributors -->
    <v-row>
      <v-container class='pa-10'>

        <h3>
          <v-icon left color='#000000DE' large>mdi-account-supervisor</v-icon>
          Contributors
        </h3>

        <v-timeline dense class='contributors-list'>
          <v-timeline-item flat v-for='(contributor, index) in contributors' v-bind:key='index'>
            <template v-slot:icon>
              <v-avatar size='60'>
                <img :src='contributor.img' :alt='"Picture of "+contributor.name'>
              </v-avatar>
            </template>
            <div v-if='contributor.role'>
              <v-chip class='role' color='success' text-color='success' x-small outlined>
                {{ contributor.role }}
              </v-chip>
            </div>
            {{ contributor.name }}
            <span class='associate-label'>{{ contributor.associate }}</span>
            <a :href='"mailto:"+contributor.mail' target='_blank'>
              <v-icon small left>mdi-email-outline</v-icon>
              {{ contributor.mail }} </a>
          </v-timeline-item>
        </v-timeline>
      </v-container>
    </v-row>

    <!-- Contacts -->
    <v-row>
      <v-container class='pa-10'>
        <h3>
          <v-icon left color='#000000DE' large>mdi-account-box-outline</v-icon>
          Contacts
        </h3>
        <p class='pa-5'>
          Dipartimento di Elettronica, Informazione e Bioingegneria <br />
          <a href='tel:+39 02 2399 3655' target='_blank'>+39 02 2399 3655</a><br />
          Politecnico di Milano<br />
          Via Ponzio 34/5<br />
          20133 Milano<br />
          Italy
        </p>
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
      websiteLogo: require('../assets/logo.png'),

      /** Contributors data */
      contributors: [
        {
          name: 'Anna Bernasconi',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/person.png'),
          mail: 'anna.bernasconi@polimi.it'
        },
        {
          name: 'Stefano Ceri',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/ceri.png'),
          mail: 'stefano.ceri@polimi.it',
          role: 'leader'
        },
        {
          name: 'Arif Canakoglu',
          associate: 'Policlinico di Milano',
          img: require('../assets/contributors/person.png'),
          mail: 'arif.canakoglu@polimi.it'
        },
        {
          name: 'Matteo Chiara',
          associate: 'Università degli Studi di Milano Statale',
          img: require('../assets/contributors/person.png'),
          mail: 'matteo.chiara@unimi.it'
        },
        {
          name: 'Luca Minotti',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/person.png'),
          mail: 'luca2.minotti@polimi.it'
        },
        {
          name: 'Pietro Pinoli',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/pinoli.png'),
          mail: 'pietro.pinoli@polimi.it'
        }
      ]
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
  font-weight: 600;
}

.contributors-list a {
  font-size: 13px;
  font-weight: normal;
  color: #0000008a !important;
}

.role {
  text-transform: uppercase;
  font-weight: 500;
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
