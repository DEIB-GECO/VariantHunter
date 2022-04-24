<!--
  Component:    ToolGuide
  Description:  Usage guide for the tool
-->

<template>
  <v-container class='mt-10'>
    <h3>
      <v-icon left color='#000000DE' large>mdi-human-greeting</v-icon>
      What is VariantHunter
    </h3>
    <p class='pl-10 pr-10'>
      <i>VariantHunter</i> is a tool for fast detection of emerging <i>SARS-CoV-2</i> variants. <br />It's an highly
      flexible and user friendly application for the systematic monitoring of the evolution of <i>SARS-CoV-2</i> both at
      global and regional level.
    </p>
    <v-container class='pl-10 pr-10 pb-5'>

      <v-expansion-panels class='mt-3' flat>

        <!-- LINEAGE INDEPENDENT -->
        <FunctionGuide title='Discover the lineage-independent search'>

          <!-- Function guide -->
          <template v-slot:default>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
          </template>

          <!-- Use cases -->
          <template v-slot:use-cases>
            <UseCase name='Use case 1'>
              <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
            </UseCase>
            <UseCase name='Use case 2'>
              <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
            </UseCase>
          </template>

        </FunctionGuide>

        <!-- LINEAGE INDEPENDENT -->
        <FunctionGuide title='Discover the lineage-specific search'>

          <!-- Function guide -->
          <template v-slot:default>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
          </template>

          <!-- Use cases -->
          <template v-slot:use-cases>
            <UseCase name='Use case 1'>
              <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
            </UseCase>
            <UseCase name='Use case 2'>
              <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' left>
            </Paragraph>
            <Paragraph src='https://media-cdn.tripadvisor.com/media/photo-s/15/a4/9b/77/legacy-hotel-at-img-academy.jpg'
                       img-max-height='300' right>
            </Paragraph>
            </UseCase>
          </template>

        </FunctionGuide>
      </v-expansion-panels>
    </v-container>

  </v-container>
</template>

<script>

import Paragraph from '@/components/general/Paragraph'
import FunctionGuide from '@/components/general/guides/tool/FunctionGuide'
import UseCase from '@/components/general/guides/tool/UseCase'

export default {
  name: 'ToolGuide',
  components: { UseCase, FunctionGuide, Paragraph }
}
</script>

<style scoped>

</style>
