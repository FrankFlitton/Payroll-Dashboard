import axios from 'axios'
// import _ from 'lodash'

export const httpFoundation = axios.create({
  baseURL: 'http://localhost:8000/'
})

export default httpFoundation
