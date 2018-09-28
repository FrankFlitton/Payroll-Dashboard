<template>
  <b-row class="mt-5 mb-5 h-100 d-flex">
    <b-col class="ui-container p-2 p-sm-5 p-absolute">
      <transition name="fade">

        <!-- data form -->
        <b-form
          v-if="!showTable"
          class="file-input-form"
        >
          <h2 class="pb-3">
            Upload Payroll File
          </h2>

          <label
            class="file-container p-3 p-sm-5"
            :class="{'error': submitError}"
          >
            <span v-if="!submitError">
              Please upload your CSV payroll file here.
            </span>
            <span v-if="submitError">
              Your CSV payroll file is invalid. Please verify and try again.
            </span>
            <input type="file" @change="updateFile($event)" />
          </label><br>
          <b-btn @click="handleSubmit()">
            Save
          </b-btn>
        </b-form>

        <!-- data table -->
        <div
          v-else-if="showTable && isCompiled"
          class="p-relative w-100 h-100"
        >
          <div class="report-wrapper">
            <h2 class="pb-3">
              Payroll Report
            </h2>
            <!-- data table -->
            <vue-good-table
              :columns="columns"
              :rows="timeSheets"
              :sort-options="{
                enabled: true
              }"
              :search-options="{
                enabled: true,
                placeholder: 'Search by employee number',
                searchFn: searchEmployees,
              }"
            />

          </div>
        </div>

        <div
          v-else
          class="loading"
      ></div>

      </transition>

    </b-col>
  </b-row>
</template>

<script>
import HTTP from '@/http'
import _ from 'lodash'
import {VueGoodTable} from 'vue-good-table'

export default {
  name: 'PayrollDashboard',
  components: {
    VueGoodTable
  },
  mounted () {
    this.getTimeSheets()
  },
  computed: {
    showTable () {
      return !!this.timeSheets.length
    }
  },
  methods: {
    updateFile (event) {
      this.form.formData.append('file', event.target.files[0])
    },
    handleSubmit () {
      this.postFile()
    },
    postFile () {
      let vm = this
      HTTP.post('/uploads/', vm.form.formData, vm.form.headers)
        .then(response => {
          vm.submitError = false
          vm.getTimeSheets()
        })
        .catch(error => {
          vm.submitError = true
          console.log(error)
        })
    },
    getTimeSheets () {
      let vm = this
      HTTP.get('/timesheet/')
        .then(response => {
          vm.timeSheets = vm.setupTimeSheets(response.data)
          console.log(`print timesheets`, vm.timeSheets)
        })
        .catch(error => {
          console.log(error)
        })
    },
    // Format the object for table viz
    setupTimeSheets (timeSheets) {
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
      submitError: false,
      isCompiled: false,
      columns: [
        {
          label: 'Employee ID',
          field: 'employee'
        },
        {
          label: 'Pay Period',
          field: 'pay_period'
        },
        {
          label: 'Pay Amount',
          field: 'pay_amount',
          sortable: true,
          sortFn: (x, y) => {
            return (x < y ? -1 : (x > y ? 1 : 0))
          }
        }
      ],
      form: {
        formData: new FormData(),
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    }
  }
}
</script>

<style lang="scss">
// Variables
$c-grey: rgba(230, 234, 236, 0.5);
$c-primary: rgb(34, 14, 218);
$c-error-bg: rgba(221, 169, 169, 0.5);
$c-error-text: rgb(241, 14, 14);
$b-radius: 5px;
$margin: 15px;

.ui-container {
  background: solid 1px $c-grey;
  box-shadow: 0px 5px 13px 5px $c-grey;
  border-radius: $b-radius;
  background: white;
  width: 100%;
  position: relative;
  min-height: 400px;

  // file upload styles
  .file-input-form {
    width: 80%;
    overflow: hidden;
    padding: $margin;
    position: absolute !important;
    display: block;
    top: 30px;
    left: 10%;
    z-index: 0;
    .file-container {
      width: 100%;
      background: $c-grey;
      border-radius: $b-radius;
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
}

// report positioning
.report-wrapper {
  top: 0;
  position: relative !important;
  width: 100%;
  z-index: 1;
}
// table style
.vgt-wrap {
  border-radius: $b-radius;
  overflow: hidden;
  .vgt-global-search, {
    background: $c-grey !important;
    padding: $margin 0;
  }
  .sorting {
    background: $c-grey !important;
    padding: $margin $margin;
  }
  .vgt-table th.sorting:after {
    border-bottom-color: $c-primary;
  }
  .vgt-table th.sorting:after {
    border-top-color: $c-primary;
  }
  tbody td {
    padding: $margin $margin;
  }
  tbody tr:nth-child(even) {
    background: rgba($c-primary, 0.03);
  }
  *:not(.magnifying-glass) {
    border: none !important;
  }
}

// error style
.error {
  background: $c-error-bg !important;
  color: $c-error-text !important;
}

// preloading animation
.loading, .loading:before, .loading:after {
  content: " ";
  background: rgba($c-primary, 0.21);
  width: 13vw;
  height: 13vw;
  margin: 0 auto;
  top: 10vw;
  left: 40vw;
  border-radius: 50%;
  position: absolute;
  opacity: 1;
  transform: scale(1)
}
.loading:before, .loading:after {
  animation: pulse 1s infinite ease;
  left: 0px;
  top: 0px;
  background: $c-primary;
}
.loading:after {
  animation: pulse 1s 0.8s infinite ease;
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
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
