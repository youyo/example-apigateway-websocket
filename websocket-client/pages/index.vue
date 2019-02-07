<template>
  <div>
    <textarea v-model="message" @keyup.enter="send" placeholder="message"></textarea>
    <button v-on:click="send">送信</button>
    <v-layout row>
      <v-card>
        <v-list>
          <v-list-tile
            v-for="item in items"
            :key=item
          >
            <v-list-tile-content>
              <v-list-tile-title v-text="item"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card>
    </v-layout>
  </div>
</template>

<script>
import { w3cwebsocket } from 'websocket'
const W3CWebSocket = w3cwebsocket

export default {
  data: function() {
    return {
      socket: new W3CWebSocket(process.env.websocketUrl),
      message: '',
      answer: '',
      items: [],
    }
  },

  created: function() {
    const self = this
    self.socket.onmessage = function(e) {
      if (typeof e.data === 'string') {
        self.answer = e.data
        self.items.push(e.data)
      }
    }
  },

  methods: {
    send: function() {
      console.log(JSON.stringify({action:'sendmassage',data:this.message}))
      this.socket.send(
        JSON.stringify({action:'sendmessage',data:this.message.replace(/\r?\n/g, '')})
      )
      this.message = ''
    }
  }
}
</script>
