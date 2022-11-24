<!--
  View:         About
  Description:  Component for the about section.
-->

<template>
  <v-container class='about'>

    <!-- Website title -->
    <v-row class='justify-center mt-5'>
      <v-col cols="12" sm="3" lg="2">
        <div class='huge-title'>
          <div class='huge-logo hidden-xs-only'>
            <v-img :src='websiteLogo' class="about-logo" max-height='150px' max-width='150px' aspect-ratio="1"/>
          </div>
          <v-img :src='websiteLogo' class='about-logo hidden-sm-and-up' max-height='80px' max-width='80px' aspect-ratio="1"/>
        </div>
      </v-col>
      <v-col cols="12" sm="5" lg="3">
        <div class='site-title huge-site-title'>
          <span class='emphasis'>Variant</span><br/>
          <span>Hunter</span>
        </div>
      </v-col>
    </v-row>

    <!-- Buttons -->
    <v-row class='justify-center mb-10'>
      <v-col cols="12" sm="4" lg="3" class="text-center">
        <router-link to='/variant_hunter'>
          <v-btn class='' color='text_var1' depressed outlined rounded>
            <v-icon left>mdi-virus-outline</v-icon>
            Go to the tool
          </v-btn>
        </router-link>
      </v-col>
      <v-col cols="12" sm="4" lg="3" class="text-center">
        <a href='https://github.com/DEIB-GECO/VariantHunter' target='_blank'>
          <v-btn class='' color='success' depressed outlined rounded>
            <v-icon left>mdi-github</v-icon>
            View on Github
          </v-btn>
        </a>
      </v-col>
    </v-row>

    <!-- Tool info -->
    <v-row class='with-separator underlined-links'>
      <ToolGuide/>
    </v-row>

    <!-- Docker info -->
    <v-row class='underlined-links'>
      <DockerGuide/>
    </v-row>

    <v-row class='justify-center mt-5'>
      <v-col cols='col-xs-12 col-sm-12 col-lg-6'>
        <v-container class='mt-5'>

          <h3 id='contributors'>
            <v-icon left color='text_var1' large>mdi-account-supervisor</v-icon>
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
        <v-container class='mt-5'>
          <h3>
            <v-icon left color='text_var1' large>mdi-account-box-outline</v-icon>
            Contacts
          </h3>
          <v-row>
          <v-col cols="12" sm="5" >
            <div class='pa-5 pb-0'><v-img alt="Logo of Politecnico di Milano" :src="require('@/assets/others/deib_logo.png')" contain max-width="250px"/></div>
          </v-col>
            <v-col cols="12" sm="7">
              <p class='pa-5'>
                <span class="font-weight-medium">Dipartimento di Elettronica, Informazione e Bioingegneria</span> <br/>
                <span class="font-weight-bold"> Politecnico di Milano</span><br/>
                <a href='tel:+39 02 2399 3655' target='_blank'>+39 02 2399 3655</a><br/>
                Via Ponzio 34/5<br/>
                20133 Milano<br/>
                Italy
              </p>
            </v-col>
          </v-row>
        </v-container>

        <v-container class='mt-5'>

          <h3>
            <v-icon left color='text_var1' large>mdi-shield-star-outline</v-icon>
            License
          </h3>
          <p class='pa-5'>
            Variant Hunter is licensed under the <span class="font-weight-bold">Apache License 2.0</span><br/>
            <span class="underlined-links text-uppercase text-caption">
              <a href="https://github.com/DEIB-GECO/VariantHunter/blob/master/LICENSE" target="_blank">
                more info...
              </a>
            </span>
          </p>
        </v-container>

        <v-container class='mt-5'>

          <h3>
            <v-icon left color='text_var1' large>mdi-account-heart</v-icon>
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
import ToolGuide from '@/components/guides/tool/ToolGuide'
import DockerGuide from '@/components/guides/docker/DockerGuide'

export default {
  name: 'About',
  components: {ToolGuide, DockerGuide},
  data() {
    return {
      /** VariantHunter logo */
      websiteLogo: require('../../assets/logo.svg'),

      /** Ack data */
      acks: [
        {
          name: 'Luca Cilibrasi',
          img: require('../../assets/contributors/person.png'),
          associate: 'Politecnico di Milano, Milan, Italy'
        },
        {
          name: 'Shay Fleishon',
          img: require('../../assets/contributors/person.png'),
          associate: 'Independent Researcher, Jerusalem, Israel'
        },
        {
          name: 'Valeria Micheli',
          img: require('../../assets/contributors/person.png'),
          associate: 'Laboratory of Clinical Microbiology, Virology and Bioemergencies, \n' +
              'ASST Fatebenefratelli, Sacco, Milan, Italy'
        }
      ],

      /** Contributors data */
      contributors: [
        {
          name: 'Pietro Pinoli',
          associate: 'Politecnico di Milano',
          img: require('../../assets/contributors/pinoli.png'),
          mail: 'pietro.pinoli@polimi.it',
          role: 'reference',
          roleColor: 'info'
        },
        {
          name: 'Luca Minotti',
          associate: 'Politecnico di Milano',
          img: require('../../assets/contributors/minotti.jpeg'),
          mail: 'minottiluca@icloud.com'
        },
        {
          name: 'Anna Bernasconi',
          associate: 'Politecnico di Milano',
          img: require('../../assets/contributors/bernasconi.jpg'),
          mail: 'anna.bernasconi@polimi.it'
        },
        {
          name: 'Arif Canakoglu',
          associate: 'Policlinico di Milano',
          img: require('../../assets/contributors/canakoglu.jpeg'),
          mail: 'arif.canakoglu@polimi.it'
        },
        {
          name: 'Matteo Chiara',
          associate: 'Università degli Studi di Milano Statale',
          img: require('../../assets/contributors/chiara.png'),
          mail: 'matteo.chiara@unimi.it'
        },
        {
          name: 'Erika Ferrandi',
          associate: 'IBIOM-CNR Bari',
          img: require('../../assets/contributors/ferrandi.png'),
          mail: 'e.ferrandi@ibiom.cnr.it'
        },
        {
          name: 'Stefano Ceri',
          associate: 'Politecnico di Milano',
          img: require('../../assets/contributors/ceri.png'),
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
  height: 100%;
  align-items: center;
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
  color: var(--v-text_var1-base) !important;
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
.about .v-expansion-panel-header, .v-dialog .v-expansion-panel-header {
  font-weight: 600;
  padding-top: 3px;
  padding-bottom: 3px;
}

.about-logo{
  background-color: white;
  border-radius: 22px;
}

.huge-logo .about-logo{
  border-radius: 35px;
}
</style>
