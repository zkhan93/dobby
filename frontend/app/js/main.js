var app = new Vue({
    el: '#app',
    data: {
        angle: 0,
        user: undefined,
        token: undefined,
        config: {
            apiKey: "AIzaSyC4ONXr_ODDwNGpRLKToAkIxHcNuD--eEw",
            authDomain: "doby-200617.firebaseapp.com",
            databaseURL: "https://doby-200617.firebaseio.com",
            projectId: "doby-200617",
            storageBucket: "doby-200617.appspot.com",
            messagingSenderId: "286200648030"
        },
        loading: false,

        started: false, 
        movement: undefined,
        distance: 'unknown distance',
        ultrasonicLooper: undefined,
    },
    mounted: function() {
        
    },
    updated: function() {},
    watch: {
        movement: function(){
            if(!this.movement)
                return
            if(this.movement.state === 'lock')
                return
            if(!this.movement.direction)
                return
            if(this.movement['direction-adjective'] === 'keep'){
                this.$http.get('/api/wheels/keep/'+this.movement.direction)
            }
            else{
                this.$http.get('/api/wheels/'+this.movement.direction)
            }
        },
        angle(){
            this.$http.get(`/api/cam/angle/${this.angle}`)
        }
    },
    methods: {
        start: function(){
            this.loading = true
            this.init()

        },
        stop: function(){
            var dirRef = firebase.database().ref('movement')
            dirRef.off('value')
            this.started = false
        },
        init: function(){
            var vm = this
            this.startSignIn(function(){
                var dirRef = firebase.database().ref('movement')
                dirRef.on('value', vm.movementListener)
                console.log('listning...')
                vm.started = true
                vm.loading = false
            })
        },
        startSignIn: function(callback){
          var vm = this
          firebase.initializeApp(this.config);
          var provider = new firebase.auth.GoogleAuthProvider();
          firebase.auth().signInWithPopup(provider).then(function(result) {
            // This gives you a Google Access Token. You can use it to access the Google API.
            vm.token = result.credential.accessToken;
            // The signed-in user info.
            vm.user = result.user;
            console.log(user)
            if(callback){
                callback()
            }else{
                vm.loading = false
            }
          }).catch(function(error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            // The email of the user's account used.
            var email = error.email;
            // The firebase.auth.AuthCredential type that was used.
            var credential = error.credential;
            console.log(errorMessage)
            if(callback){
                callback()
            }else{
                vm.loading = false
            }
          });
        },

        movementListener: function(snapshot){
            this.movement = snapshot.val()
        },
        hitWheelsApi: function(direction){
            this.$http.get('/api/wheels/'+direction).
            then(response => {
                console.log(response)
            }, error=>{
                console.log(error)
            })
        },

        startUltrasonicLooper: function(){
            this.ultrasonicLooper = setInterval(this.hitUltrasonicApi, 1000);
        },
        stopUltrasonicLooper: function(){
            clearInterval(this.ultrasonicLooper)
            this.ultrasonicLooper = undefined
        },
        toggleUltrasonic: function(){
            if(this.ultrasonicLooper)
                this.stopUltrasonicLooper()
            else
                this.startUltrasonicLooper()
        },
        hitUltrasonicApi: function(){
            var vm = this
          this.$http.get('/api/path/').
            then(response => {
                if(response.body.res==='success'){
                    vm.distance = response.body.distance + ' ' + response.body.unit
                }
            }, error=>{
                console.log(error)
            })  
        },

        hitCamApi: function(direction){
            this.$http.get('/api/cam/'+direction).
            then(response => {
                console.log(response)
            }, error=>{
                console.log(error)
            })
        }
    },
})