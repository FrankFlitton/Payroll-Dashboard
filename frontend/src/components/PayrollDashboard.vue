<template>
  <b-row class="mt-5 mb-5 h-100 d-flex">

    <transition name="fade">
      <b-col
        v-if="showTable"
        class="ui-container w-100 p-2 p-sm-5 p-relative mb-5"
        cols="12"
      >

        <!-- Loading Icon -->
        <transition name="fade">
          <div
            v-if="!isCompiled || (!showTable)"
          >
            <div class="loading"></div>
          </div>
          <div
            v-if="showTable && isCompiled && isInit"
          >
            <reportTable
              v-if="showTable && isCompiled"
              :rows="timeSheets"
            ></reportTable>
          </div>
        </transition>

      </b-col>
    </transition>

    <b-col class="ui-container w-100 p-2 p-sm-3 p-relative mb-5" cols="12">

        <!-- upload form -->
        <b-form
          class="file-input-form"
        >
          <h2 class="pb-4">
            Upload Payroll File
          </h2>

          <label
            class="file-container p-3"
            :class="{'error': errorClass }"
          >

            <!-- CTA -->
            <span v-if="!submitError && !form.fileSelected">
              Please upload your CSV payroll file here.<br>
            </span>

            <!-- File Status -->
            <span v-if="submitError.length">
              {{submitError}} <br>
              <small>{{form.fileSelected}}</small>
            </span>
            <span v-else-if="form.fileSelected">
              {{form.fileSelected}} is selected.<br>
              <small>{{form.fileSelected}}</small>
            </span>

            <input type="file" @change="updateFile($event)" />
          </label><br>
          <b-btn
            @click="handleSubmit()"
            varient="primary"
            class="mb-5"
          >
            Save
          </b-btn>
        </b-form>
    </b-col>
  </b-row>
</template>

<script>
import HTTP from '@/http'
import _ from 'lodash'
import reportTable from '@/components/ReportTable'

export default {
  name: 'PayrollDashboard',
  components: {
    reportTable
  },
  mounted () {
    this.getTimeSheets()
  },
  computed: {
    showTable: function () {
      return !!this.timeSheets.length
    },
    errorClass: function () {
      return !!this.submitError.length
    }
  },
  methods: {
    updateFile (event) {
      // check for csv file extension
      const csvCheck = event.target.files[0]
        ? _.lowerCase(event.target.files[0].name.split('.').reverse()[0])
        : null

      this.form.fileSelected = ''
      this.submitError = ''

      if (csvCheck === 'csv') {
        // prep form data
        this.form.formData.append('file', event.target.files[0])
        this.form.fileSelected = event.target.files[0].name
      } else {
        // report error
        this.submitError = 'Please select a CSV file.'
        this.form.fileSelected = event.target.files[0]
          ? event.target.files[0].name
          : 'no file selected'
      }
    },
    handleSubmit () {
      if (!this.submitError) {
        this.postFile()
      }
    },
    postFile () {
      let vm = this
      vm.submitError = ''
      HTTP.post('/uploads/', vm.form.formData, vm.form.headers)
        .then(response => {
          vm.getTimeSheets()
        })
        .catch(error => {
          vm.submitError = error.response.data[0]
          console.log(error)
        })
    },
    getTimeSheets () {
      let vm = this
      HTTP.get('/timesheet/')
        .then(response => {
          // Used for BE data check, hides form
          this.isInit = true

          // Set up data for display
          vm.timeSheets = vm.setupTimeSheets(response.data)
          console.log(`print timesheets`, vm.timeSheets)
        })
        .catch(error => {
          console.log(error)
        })
    },
    // Format the object for table viz
    setupTimeSheets (timeSheets) {
      this.isCompiled = false

      // Set up the data to process
      timeSheets.map(sheet => {
        sheet.employee = sheet.employee.id
        sheet.compensation = sheet.job_group.compensation
        sheet.pay_amount = sheet.job_group.compensation * sheet.hours_worked
        return sheet
      })
      let consolodatedTimeSheets = this.consolidateTimeSheets(timeSheets)
      return consolodatedTimeSheets
    },
    consolidateTimeSheets (timeSheets) {
      let compiledSheet = []
      // Seperate by payPeriod
      let employeeId = _.groupBy(timeSheets, 'employee')
      employeeId = _.forEach(employeeId, (value, key) => {
        let employeeIdNum = key

        // Seperate by Employee Id
        employeeId[key] = _.groupBy(employeeId[key], 'pay_period')

        // Pack timesheet per employee per paydate
        for (let payPeriod in employeeId[key]) {
          let tempObj = {}
          tempObj.pay_amount = 0
          tempObj.pay_period = payPeriod
          tempObj.employee = employeeIdNum

          // Sum total pay
          _.forEach(employeeId[key][payPeriod], value => {
            tempObj.pay_amount += value.pay_amount
          })

          compiledSheet.push(tempObj)
        }
      })

      // Reveals table
      this.isCompiled = true

      return compiledSheet
    },
    searchEmployees (row, col, cellValue, searchTerm) {
      return row.employee === searchTerm
    }
  },
  data () {
    return {
      timeSheets: [],
      submitError: '',
      isCompiled: false,
      isInit: true,
      loadSlow: false, // change to see loading icon
      form: {
        formData: new FormData(),
        fileSelected: '',
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    }
  }
}
</script>

<style lang="scss">
@import 'static/variables.scss';

// Container
.ui-container {
  background: solid 1px $c-grey;
  box-shadow: 0px 5px 13px 5px $c-grey;
  border-radius: $b-radius;
  background: white;
  width: 100%;
  position: relative;
}

// file upload styles
.file-input-form {
  width: 80%;
  overflow: hidden;
  padding: $margin;
  position: relative;
  display: block;
  top: 30px;
  left: 10%;
  z-index: 0;
  .file-container {
    width: 80%;
    background: $c-grey;
    border-radius: $b-radius;
    overflow: hidden;
    position: relative;
    left: 0;
    &:hover {
      background: rgba($c-primary, 0.2)
    }
  }
  [type=file] {
    cursor: pointer;
    display: flex;
    font-size: 999px;
    filter: alpha(opacity=0);
    min-height: 100%;
    min-width: 100%;
    opacity: 0;
    position: absolute;
    right: 0;
    text-align: right;
    top: 0;
  }
  .btn {
    margin-top: 30px;
    width: 120px;
    background: $c-primary;
    position: relative;
    z-index: 999;
  }
}

// report positioning
.report-wrapper {
  top: 0;
  // position: relative !important;
  z-index: 1;
}

// error style
.error {
  background: $c-error-bg !important;
  color: $c-error-text !important;
}

// preloading animation
.loading, .loading:before {
  content: " ";
  background: rgba($c-primary, 0.34);
  width: 13vw;
  height: 13vw;
  margin: 0 auto;
  top: 15vw;
  left: 50%;
  margin-left: -7.5vw;
  border-radius: 50%;
  position: absolute;
  transform: scale(1);
}
.loading:before  {
  animation: pulse 1s infinite ease-out;
  left: 0px;
  top: 0px;
  margin-left: 0;
  background: rgba($c-primary, 1);
}
.loading:after {
  animation: pulse 1s -0.6s infinite ease-out;
}
@keyframes pulse {
    0% {
      opacity: 1;
      transform: scale(0.32)
    }
    100% {
      opacity: 0;
      transform: scale(1)
    }
}

// transition animation
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0 !important;
}
</style>
