<template>
  <div class="about">
        <b-form @submit="clickJoinRoom" inline>
        <label class="sr-only" for="inlineFormInputName2">Name</label>
        <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Room Name" v-model="room_name"/>
        <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
        <b-button  type="submit" variant="primary">Create</b-button>
        </b-form>
        <b-form @submit="sendRoomMessage" inline>
        <label class="sr-only" for="inlineFormInputName2">Name</label>
        <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Message" v-model="message"/>
        <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
        <b-button type="submit" variant="primary">Message Send</b-button>
        </b-form>
    <b-container class="bv-example-row">
        <b-row align-h="end">
             <b-col><b-table striped hover :items="messages" ></b-table></b-col>
            <b-col cols="4"><b-table :small="true" striped hover @row-clicked="clickonRow" :items="user_rooms"></b-table></b-col>
        </b-row>
        <b-row>
            <b-col cols="4"><b-table striped hover :items="tester"></b-table></b-col>
        </b-row>
    </b-container>

  </div>
</template>
<script>
    import Vuex from "vuex";
    export default {
        data() {
            return {
                test: {},
                room: '',
                tester: [{name: 'a'}, {name: 'This is <i>raw <strong>HTML</strong></i> <span style="color:red">content</span>'}],
                room_name: null,
                message: 'Hi',
                messages: [],
                sid: null,
                selected: null,
                show: true
            }
        },
        created() {
            console.log(this.user_name)
            this.$options.sockets.response = (data) => {
                // console.log(data)
                if (data.sid != this.sid) {
                    this.messages.push(data)
                }
            }
        },
        sockets: {
            connect: function () {
                console.log('socket connected')
                this.$options.sockets.rooms = (data) => {
                    // console.log(data)
                    this.sid = data.sid
                }
            },
        },
        methods: {
            clickJoinRoom: function (val) {
                this.$socket.emit('join', {'room': this.room_name})
                this.room_select.push({'value':this.room_name, 'text':this.room_name})
                // this.$store.dispatch('getAllRooms')
            },
            sendRoomMessage: function (message) {
                // console.log(this.message)
                // console.log(this.room_name)
                this.$socket.emit('room_event', {'room': this.room_name, 'data': this.message})
            },
            clickonRow: function (item, index, event) {
                this.$socket.emit('join', {'room': item.name})
                this.room_name = item.name
            }
        },
        computed: {
            rooms() {
                return this.$store.state.rooms
            },
            user_rooms() {
                return this.$store.state.user_rooms
            },
            user_name() {
                return this.$store.user_name
            }
        }
    }
</script>
