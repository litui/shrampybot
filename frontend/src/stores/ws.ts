import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { useAuthStore } from './auth'
import { useLocalStorage } from '@vueuse/core'
import { isProxy } from 'vue'

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
    const socket = {} as typeof WebSocket
    const connected = false
    return {
      socket: socket as any,
      connected: connected as any,
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
            reject(new Error('Maximum number of attempts exceeded.'))
          } else if (this.socket.readyState === this.socket.OPEN) {
            clearInterval(interval)
            resolve(null)
          }
          currentAttempt++
        }, intervalTime)
      })
    },
    async sendData(jsonData: Record<string, any>) {
      // Trigger the wait for open connection if we've jumped the gun
      if (this.socket.readyState !== this.socket.OPEN || this.connected === false) {
        try {
          await this.waitForOpenConnection()
          console.log(this.socket)
          this.socket.send(JSON.stringify(jsonData))
        } catch (err) {
          console.error(err)
        }
      } else {
        this.socket.send(JSON.stringify(jsonData))
      }
    },
    socketOnOpenCallback(event: Event) {
      console.info('Websocket connected.')
      this.connected = true
    },
    socketOnMessageCallback(event: MessageEvent) {
      const jsonData = JSON.parse(event.data)
      console.info(jsonData)

      if (jsonData.class === 'sb.users.self') {
        const UserStore = useUserStore()

        UserStore.setSelf(jsonData.data)
      } else if (jsonData.class === 'sb.ping') {
        this.socket.send(
          JSON.stringify({
            class: 'vue.pong',
          }),
        )
      } else if (jsonData.class === 'sb.users.services.status') {
        const AuthStore = useAuthStore()

        AuthStore.userServicesStatus[jsonData.service] = jsonData.data
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
      try {
        this.socket.close()
      } catch (err) {
        // test
      }
      if (!token) {
        console.warn('No login credentials. Cannot establish websocket connection.')
        return
      }
      this.socket = new WebSocket(echoSocketUrl, ['jwt_bearer', token])

      this.socket.onopen = (event) => this.socketOnOpenCallback(event)
      this.socket.onmessage = (event) => this.socketOnMessageCallback(event)
      this.socket.onclose = (event) => this.socketOnCloseCallback(event)
      this.socket.onerror = (event) => this.socketOnErrorCallback(event)
    },
  },
})
