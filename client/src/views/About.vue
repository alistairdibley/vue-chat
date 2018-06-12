<template>
  <div class="about">
    <b-form @submit="clickJoinRoom" inline>
      <label class="sr-only" for="inlineFormInputName2">Name</label>
      <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Room Name" v-model="room_name"/>
      <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
      <b-button  type="submit" variant="primary">Join</b-button>
    </b-form>
    <b-form @submit="sendRoomMessage" inline>
      <label class="sr-only" for="inlineFormInputName2">Name</label>
      <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Message" v-model="message"/>
      <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
      <b-form-select :v-model="selected" :options="room_select" />
      <b-button type="submit" variant="primary">Message Send</b-button>
    </b-form>
    <b-table striped hover @row-clicked="clickonRow" :items="rooms"></b-table>
    <b-table striped hover :items="messages" ></b-table>

  </div>
</template>
<script>
    import Vuex from "vuex";
    export default {
        data() {
            return {
                test: {},
                room: '',
                room_name: null,
                message: 'Hi',
                messages: [],
                sid: null,
                room_select: [
                    {text: 'Select One', value: null, disabled:true},
                    {text: 'Tester', value: 'tester', selected:true},
                    {text: 'Tester2', value: 'tester2',},
                ],
                selected: null,
                show: true
            }
        },
        created() {
            this.$store.dispatch('getAllRooms')
        },
        sockets: {
            connect: function () {
                console.log('socket connected')
                this.$options.sockets.response = (data) => {
                    if (data.sid != this.sid) {
                        this.messages.push(data)
                    }
                },
                this.$options.sockets.rooms = (data) => {
                    console.log(data)
                    this.sid = data.sid
                }
            },
        },
        methods: {
            clickJoinRoom: function (val) {
                this.$socket.emit('join', {'room': this.room_name})
                this.room_select.push({'value':this.room_name, 'text':this.room_name})
                this.$store.dispatch('getAllRooms')
            },
            sendRoomMessage: function (message) {
                console.log(this.selected)
                console.log(this.room_name)
                this.$socket.emit('room_event', {'room': this.room_name, 'data': this.message})
            },
            clickonRow: function (item, index, event) {
                console.log(item)
            }
        },
        computed: {
            rooms() {
                return this.$store.state.rooms
            }
        }

    }
</script>
