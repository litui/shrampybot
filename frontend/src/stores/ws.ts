import { defineStore } from 'pinia'
import { useUserStore } from './user'

interface WSStoreRecord {
  socket: WebSocket
  connected: boolean
}

const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
const port = window.location.port
const echoSocketUrl = socketProtocol + '//' + window.location.hostname + ':' + port + '/ws/service/'

// const AuthStore = useAuthStore()

export const useWSStore = defineStore('ws', {
  state: () => {
    return {
      socket: {} as WebSocket,
      connected: false,
    } as WSStoreRecord
  },
  actions: {
    waitForOpenConnection() {
      return new Promise((resolve, reject) => {
        const maxNumberOfAttempts = 10
        const intervalTime = 200

        let currentAttempt = 0
        const interval = setInterval(() => {
          if (currentAttempt > maxNumberOfAttempts - 1) {
            clearInterval(interval)
            reject(new Error('Maximum number of attempts exceeded.'));
          } else if (this.socket.readyState === this.socket.OPEN) {
            clearInterval(interval)
            resolve(null)
          }
          currentAttempt++
        }, intervalTime)
      })
    },
    async sendMessage(message: string) {
      if (this.socket.readyState !== this.socket.OPEN) {
        try {
          await this.waitForOpenConnection()
          this.socket.send(message)
        } catch (err) {
          console.error(err)
        }
      } else {
        this.socket.send(message)
      }
    },
    socketOnOpenCallback(event: Event) {
      console.info('Websocket connected.')
      this.connected = true

      this.socket.send(
        JSON.stringify({
          class: 'vue.subscribe',
          group: 'frontend',
        }),
      )
    },
    socketOnMessageCallback(event: MessageEvent) {
      const jsonData = JSON.parse(event.data)

      if (jsonData.class === 'sb.users.self') {
        const UserStore = useUserStore()

        UserStore.setSelf(jsonData.data)
      }
    },
    socketOnCloseCallback(event: CloseEvent) {
      console.warn('Websocket disconnected.')
      this.$state.connected = false
    },
    socketOnErrorCallback(event: Event) {
      event
    },
    connectSocket(token: string) {
      this.socket = new WebSocket(echoSocketUrl, ['access_token', token])

      this.socket.onopen = (event) => this.socketOnOpenCallback(event)
      this.socket.onmessage = (event) => this.socketOnMessageCallback(event)
      this.socket.onclose = (event) => this.socketOnCloseCallback(event)
      this.socket.onerror = (event) => this.socketOnErrorCallback(event)
    },
  },
})
