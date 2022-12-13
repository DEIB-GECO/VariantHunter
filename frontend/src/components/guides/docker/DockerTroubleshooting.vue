<!--

  Component:    DockerTroubleshooting
  Description:  Troubleshooting guide

  Props:
  └── value: Value variable for binding of the flag to show the dialog

-->

<template>
  <v-dialog v-model='showDialog' max-width='1100' transition='dialog-bottom-transition'>
    <v-card>
      <!-- Dialog title -->
      <v-toolbar color='f_primary' class='dialog-title' dark flat>
        <v-icon left large>mdi-lifebuoy</v-icon>
        Troubleshooting
      </v-toolbar>

      <!-- Dialog content -->
      <v-card-text class='text-s-center black--text dialog-text underlined-links'>
        <slot>
          <v-expansion-panels class='mt-3' flat>

            <!---- SQLITE MEMORY ERROR ---->
            <v-expansion-panel>
              <v-expansion-panel-header>
                <v-col class='col-auto'>
                  <v-icon left color='text_var1'>mdi-content-save</v-icon>
                </v-col>
                <v-col>
                  I got <span class='monospaced red--text'>sqlite3.OperationalError: database or disk is full</span>
                  or <span class='monospaced red--text'>sqlite3. DatabaseError: database disk image is malformed</span>
                  during the execution or a similar memory-related error
                </v-col>
              </v-expansion-panel-header>
              <v-expansion-panel-content class='steps'>
                <p>This issue is probably due to the fact that there is not enough free space on the device to run <i>Variant
                  Hunter</i>.</p>

                <ul>

                  <li>
                    First check if there is still free storage space left on the device.
                    <ul>
                      <li>
                        <b>If so</b>, then you may have run out of resources that are allocated to the <i>Docker
                        Engine</i>
                        (64GB by default).
                        <ul>
                          <li>
                            Consider reducing the amount of data imported into the tool (by specifying more restrictive
                            <span class='monospaced'>LOCATIONS</span>,
                            <span class='monospaced'>START_DATE</span> and
                            <span class='monospaced'>END_DATE</span> parameters).
                          </li>
                          <li>
                            Alternatively, you can increase the allocated resources from Docker settings:
                            go to <i> Preferences > Resources: Advanced </i> and increase the value for (maximum) <i>"Disk
                            image size"</i>. Then press <i>"Apply & Restart"</i>.<br/>
                            Notice that this amount of storage space must then also be actually available on the device.
                            <v-img :src='dockerSettingsImg' alt='Screenshot to illustrate the steps to be performed'
                                   contain max-height='300' class="rounded"/>
                          </li>
                        </ul>

                      </li>

                      <li>
                        <b>If not</b>, then you need more storage.<br/>
                        <ul>
                          <li>
                            Consider reducing the amount of data imported into the tool (by specifying more restrictive
                            <span class='monospaced'>LOCATIONS</span>,
                            <span class='monospaced'>START_DATE</span> and
                            <span class='monospaced'>END_DATE</span> parameters).
                          </li>
                        </ul>

                      </li>
                    </ul>
                  </li>
                </ul>

              </v-expansion-panel-content>
            </v-expansion-panel>

            <!---- DB RELOADING PROBLEM ---->
            <v-expansion-panel>
              <v-expansion-panel-header>
                <v-col class='col-auto'>
                  <v-icon left color='text_var1'>mdi-database-sync</v-icon>
                </v-col>
                <v-col>
                  I cannot generate the database. I got <span
                    class='monospaced info--text'>database overwrite skipped</span> in the console
                </v-col>
              </v-expansion-panel-header>
              <v-expansion-panel-content class='steps'>
                <ul>

                  <li>
                    <p>
                      When you specify <span class='monospaced'>DB_PATH</span>, and a database already
                      exists in the specified directory, then all the params are ignored and the existing database is
                      loaded. <br/>
                      <b>To prevent this, please specify also <span class='monospaced'>REGENERATE=true</span>.</b>
                    </p>
                    <p>
                      Notice that this would delete the existing database.
                    </p>
                  </li>
                  <li>
                    If you are not specifying the <span class='monospaced'>DB_PATH</span> parameter,
                    then remember that if the passed parameters have not changed since the last launch
                    of the container, Docker will not regenerate the container but will simply restart it.<br/>
                    <b>To prevent this, please specify also <span class='monospaced'>REGENERATE=true</span>.</b>
                  </li>
                  <li>
                    Another possibility is that you have aborted the process while generating the
                    database or have forced the shutdown by preventing gracefully stop.<br/>
                    <b>To solve this, please specify also <span class='monospaced'>REGENERATE=true</span>.</b>
                  </li>
                </ul>
              </v-expansion-panel-content>
            </v-expansion-panel>

            <!---- TIME PROBLEM ---->
            <v-expansion-panel>
              <v-expansion-panel-header>
                <v-col class='col-auto'>
                  <v-icon left color='text_var1'>mdi-clock-outline</v-icon>
                </v-col>
                <v-col>
                  Generating the database is taking a long time
                </v-col>
              </v-expansion-panel-header>
              <v-expansion-panel-content class='steps'>

                <p>
                  <b>It is strongly recommended to import into the tool only the data of
                    interest for the intended analysis</b> (by specifying
                  <span class='monospaced'>LOCATIONS</span>,
                  <span class='monospaced'>START_DATE</span> and
                  <span class='monospaced'>END_DATE</span>),
                  as the database generation may require <u>significant time and storage resources</u>.
                </p>

                <i>Consider that, on a standard machine (macOS, 4 cores, 16GB RAM), generating a database starting
                  from:</i>
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

                <p>
                  <b>It is also suggested to always export the database file</b> by specifying the <span
                    class='monospaced'>DB_PATH</span>
                  parameter, so that the Docker container can be restarted instantaneously in the next sessions
                  (no need to regenerate the database from the <span class='monospaced'>.tsv</span> file).</p>
                <p>
                  This operation may slow down the procedure <i>(order of 3 hrs on the above configuration
                  involving ~10M sequences)</i>.
                  For complex analyses, it is suggested to generate the database when the machine is not in use
                  (e.g. overnight).
                </p>

              </v-expansion-panel-content>
            </v-expansion-panel>

            <!---- MEMORY PROBLEM ---->
            <v-expansion-panel>
              <v-expansion-panel-header>
                <v-col class='col-auto'>
                  <v-icon left color='text_var1'>mdi-sd</v-icon>
                </v-col>
                <v-col>
                  Database generation is taking a lot of storage memory
                </v-col>
              </v-expansion-panel-header>
              <v-expansion-panel-content class='steps'>

                <p>
                  <b>It is strongly recommended to import into the tool only the data of
                    interest for the intended analysis</b> (by specifying
                  <span class='monospaced'>LOCATIONS</span>,
                  <span class='monospaced'>START_DATE</span> and
                  <span class='monospaced'>END_DATE</span>),
                  as the database generation may require <u>significant time and storage resources</u>.
                </p>

                <i>Consider that, on a standard machine (macOS, 4 cores, 16GB RAM), generating a database starting
                  from:</i>
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

                <p>
                  <b>It is also suggested to always export the database file</b> by specifying the <span
                    class='monospaced'>DB_PATH</span>
                  parameter, so that the Docker container can be restarted instantaneously in the next sessions
                  (no need to regenerate the database from the <span class='monospaced'>.tsv</span> file).</p>
                <p>
                  This operation may slow down the procedure <i>(order of 3 hrs on the above configuration
                  involving ~10M sequences)</i>.
                  For complex analyses, it is suggested to generate the database when the machine is not in use
                  (e.g. overnight).
                </p>

              </v-expansion-panel-content>
            </v-expansion-panel>

            <!---- OTHER ---->
            <v-expansion-panel>
              <v-expansion-panel-header class=' mt-3'>
                <v-col class='col-auto'>
                  <v-icon left color='text_var1'>mdi-magnify</v-icon>
                </v-col>
                <v-col>
                  My problem is not listed
                </v-col>
              </v-expansion-panel-header>
              <v-expansion-panel-content class='steps'>

                <p>
                  If your problem is not listed above, then please contact us. <br/>
                  Let us know your problem and we will try to fix it as soon as possible.
                </p>
                <v-btn color='success' small depressed outlined rounded @click.native='showContacts()'>
                  <v-icon left>mdi-email-fast</v-icon>
                  go to the contact list
                </v-btn>
              </v-expansion-panel-content>
            </v-expansion-panel>

          </v-expansion-panels>
        </slot>
      </v-card-text>

      <!-- Dialog actions -->
      <v-card-actions class='justify-end'>
        <v-btn text @click='showDialog = false'>
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  name: 'DockerTroubleshooting',

  props: {
    /** Value variable for binding of the flag to show the dialog */
    value: {}
  },

  data() {
    return {
      /** Docker settings image */
      dockerSettingsImg: require('../../../assets/troubleshooting/docker_settings.png')
    }
  },

  computed: {

    /** Flag to show/hide the dialog */
    showDialog: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('input', val)
      }
    }
  },

  methods: {
    /** Go to the contact section by hiding all the dialogs */
    showContacts() {
      this.showDialog = false
      document.getElementById('contributors').scrollIntoView()
    }
  }
}
</script>

<style scoped>

.steps li::marker {
  font-size: 26px;
}

.steps li {
  margin-bottom: 9px;
  margin-top: 9px;
}

</style>
