import axios from 'axios'

var instance = axios.create({
  timeout: 1000 * 12,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  withCredentials: true
})

export default instance

 