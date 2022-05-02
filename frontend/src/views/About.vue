<!--
  View:         About
  Description:  Component for the about section.
-->

<template>
  <v-container class='about'>

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

    <!-- Tool info -->
    <v-row  class='with-separator underlined-links'>
      <ToolGuide />
    </v-row>

    <!-- Docker info -->
    <v-row class='underlined-links'>
      <DockerGuide />
    </v-row>

    <v-row class='justify-center mt-5'>
      <v-col cols='col-xs-12 col-sm-12 col-lg-6'>
        <v-container class='mt-10'>

          <h3 id='contributors'>
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
                <v-chip class='role' :color=contributor.roleColor :text-color=contributor.roleColor x-small outlined>
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
      </v-col>
      <v-col cols='col-xs-12 col-sm-12 col-lg-6'>
        <v-container class='mt-10'>
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
        <v-container class='mt-10'>

          <h3>
            <v-icon left color='#000000DE' large>mdi-account-heart</v-icon>
            Acknowledgements
          </h3>

          <v-timeline dense class='contributors-list'>
            <v-timeline-item flat v-for='(contributor, index) in acks' v-bind:key='index'>
              <template v-slot:icon>
                <v-avatar size='60'>
                  <img :src='contributor.img' :alt='"Picture of "'>
                </v-avatar>
              </template>
              {{ contributor.name }}
              <span class='associate-label'>{{ contributor.associate }}</span>
            </v-timeline-item>
          </v-timeline>
        </v-container>
      </v-col>
    </v-row>

  </v-container>

</template>

<script>
import ToolGuide from '@/components/general/guides/tool/ToolGuide'
import DockerGuide from '@/components/general/guides/docker/DockerGuide'

export default {
  name: 'About',
  components: { ToolGuide, DockerGuide },
  data () {
    return {
      /** VariantHunter logo */
      websiteLogo: require('../assets/logo.png'),

      /** Ack data */
      acks: [
        {
          name: 'Luca Cilibrasi',
          img: require('../assets/contributors/person.png'),
          associate: 'Politecnico di Milano, Milan, Italy'
        },
        {
          name: 'Shay Fleishon',
          img: require('../assets/contributors/person.png'),
          associate: 'Independent Researcher, Jerusalem, Israel'
        },
        {
          name: 'Valeria Micheli',
          img: require('../assets/contributors/person.png'),
          associate: 'Laboratory of Clinical Microbiology, Virology and Bioemergencies, \n' +
            'ASST Fatebenefratelli, Sacco, Milan, Italy'
        }
      ],

      /** Contributors data */
      contributors: [
        {
          name: 'Pietro Pinoli',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/pinoli.png'),
          mail: 'pietro.pinoli@polimi.it',
          role: 'reference',
          roleColor: 'info'
        },
        {
          name: 'Luca Minotti',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/minotti.jpeg'),
          mail: 'luca2.minotti@mail.polimi.it'
        },
        {
          name: 'Anna Bernasconi',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/bernasconi.jpg'),
          mail: 'anna.bernasconi@polimi.it'
        },
        {
          name: 'Arif Canakoglu',
          associate: 'Policlinico di Milano',
          img: require('../assets/contributors/canakoglu.jpeg'),
          mail: 'arif.canakoglu@polimi.it'
        },
        {
          name: 'Matteo Chiara',
          associate: 'Università degli Studi di Milano Statale',
          img: require('../assets/contributors/chiara.png'),
          mail: 'matteo.chiara@unimi.it'
        },
        {
          name: 'Erika Ferrandi',
          associate: 'IBIOM-CNR Bari',
          img: require('../assets/contributors/ferrandi.png'),
          mail: 'e.ferrandi@ibiom.cnr.it'
        },
        {
          name: 'Stefano Ceri',
          associate: 'Politecnico di Milano',
          img: require('../assets/contributors/ceri.png'),
          mail: 'stefano.ceri@polimi.it',
          role: 'leader',
          roleColor: 'success'
        }
      ]
    }
  }
}
</script>

<style scoped>

/* Huge logo styling */
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

/* Add a border to separate the sections */
.with-separator {
  border-top: 2px solid rgba(0, 0, 0, 0.12);
}

/* Contributors/Ack styling */
.associate-label {
  display: block;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: normal;
  white-space: pre-wrap;
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

</style>

<style>

/* Revert usual behavior for links */
.underlined-links a {
  color: var(--secondary-color) !important;
}

/** Fake links styling */
.fake-link {
  text-decoration: underline;
  cursor: pointer;
  font-weight: 500;
}

/* Sections styling */
h3 {
  font-size: 20px;
  font-weight: 900;
  text-transform: uppercase;
}
h4 {
  font-weight: 900;
  text-transform: uppercase;
}

/* Monospaced styling */
.monospaced {
  font-family: monospace !important;
  padding-left: 5px;
  padding-right: 5px;
  text-transform: initial !important;
}

/** Full width expand-collapse button */
.full-width-button {
  width: 100% !important;
}

/* Expansion panel header style */
.about .v-expansion-panel-header, .v-dialog .v-expansion-panel-header{
  font-weight: 600;
  padding-top: 3px;
  padding-bottom: 3px;
}

</style>
