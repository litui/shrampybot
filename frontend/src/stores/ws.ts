import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { useAuthStore } from './auth'
import { useLocalStorage } from '@vueuse/core'
import { WSStoreRecord } from '../data/sbTypes'

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
      connected: connected as boolean,
      openRequestIds: [] as Array<number>,
      unexpectedMessageIds: [] as Array<number>,
      messageQueue: [] as Array<object>,
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

      const reqId = new Date().getTime()
      this.$state.openRequestIds.push(reqId)
      this.socket.send(
        JSON.stringify({
          action: 'retrieve_self',
          request_id: reqId,
        }),
      )
    },
    handleResponse(data: any) {
      // Do nothing here by default - this is for action hooks
      data
    },
    handleUnexpected(data: any) {
      // Do nothing here by default - this is for action hooks
      data
    },
    setMessageHandled(data: any) {
      let index = this.unexpectedMessageIds.indexOf(data.request_id)
      if (index >= 0) {
        delete this.unexpectedMessageIds[index]
      }

      index = this.messageQueue.indexOf(data)
      if (index >= 0) {
        delete this.messageQueue[index]
      }
    },
    socketOnMessageCallback(event: MessageEvent) {
      const jsonData = JSON.parse(event.data)
      console.info(jsonData)
      // expected responses
      if (this.openRequestIds.indexOf(jsonData.request_id) >= 0) {
        console.debug(`Received inbound message matching Request ID ${jsonData.request_id}`)
        delete this.openRequestIds[this.openRequestIds.indexOf(jsonData.request_id)]
        this.handleResponse(jsonData)
      } else {
        console.debug(`Received new upstream '${jsonData.action}' with Request ID ${Number(jsonData.request_id)}`)
        this.unexpectedMessageIds.push(jsonData)
        this.handleUnexpected(jsonData)
      }

    //   } else if (jsonData.class === 'sb.users.services.status') {
    //     const AuthStore = useAuthStore()

    //     AuthStore.userServicesStatus[jsonData.service] = jsonData.data
    //   }
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
