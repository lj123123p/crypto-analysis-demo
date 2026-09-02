import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

export function fetchHistory(coin, days = 90) {
  return http.get('/history/' + coin, { params: { days } }).then(r => r.data)
}

export function postAnalyze(coin, news) {
  return http.post('/analyze', { coin, news }).then(r => r.data)
}

export function fetchCoins() {
  return http.get('/coins').then(r => r.data)
}