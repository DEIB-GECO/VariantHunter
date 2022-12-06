<!--

  Component:    ResultIntro
  Description:  Result intro step of the app-tour

-->

<template>
  <v-col cols="12">
    <feature-intro step="result" :alt-steps="['tour','explorer']" next-step="filters" icon="mdi-human-greeting-variant" beginning>
      <template>
        <div class="pl-4">
          <div>
            <div class="text-uppercase text-body-5 font-weight-black letter-spacing-1">Looks like you are new here</div>
            <div class="text-h5 font-weight-bold">Let's continue the tour of the app!</div>
            <div class="text-body-2 mb-6">
              Discover the potential of Variant Hunter with a very quick tour of the result panel.<br/>
              Or, alternatively, see the
              <router-link class="fake-link" :to="{ name: 'About'}">About section</router-link>
              for more details.
            </div>
          </div>
        </div>
      </template>
    </feature-intro>
  </v-col>
</template>

<script>
import FeatureIntro from "@/components/general/basic/FeatureIntro";

export default {
  name: "ResultIntro",
  components: {FeatureIntro},
}
</script>

<style scoped>

</style>