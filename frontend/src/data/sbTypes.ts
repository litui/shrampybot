// Model-based types
import models from '../../model-ts/all.ts'

// Websocket-related types:

export interface WSStoreRecord {
  socket: WebSocket | null
  connected: boolean
  openRequestIds: Array<number>
  unexpectedMessageIds: Array<number>
  messageQueue: Array<object>
}

export interface WSMessage {
  action: string
  request_id: number
  pk?: number
  object_type?: string
  data?: Record<string, any>
}

export interface WSResponse {
  action: string
  data?: Record<string, any>
  errors: Array<string>
  request_id?: number
  response_status?: number
}