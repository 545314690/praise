<template>
  <div class="content1" style="text-align: left">
    <div style="margin-bottom: 10px;">
      <button :class="showType=='按首字母'?'selectLetter':'letter'" @click="showType='按首字母'">按首字母</button>
      <button :class="showType=='按顺序'?'selectLetter':'letter'" @click="showType='按顺序'">按顺序</button>
    </div>
    <div v-if="showType =='按首字母'"  style="margin-bottom: 10px">
       <span v-for="letter in letters" :class="letter==selectLetter?'selectLetter':'letter'" @click="changeLetter(letter)">
          {{letter}}
        </span>
    </div>
    <div v-if="showType =='按顺序'" style="margin-bottom: 10px">
       <span v-for="order in orders" :class="order==selectOrder?'selectLetter':'letter'" @click="changeOrder(order)">
          {{order.name}}
        </span>
    </div>
    <span style="overflow: scroll;width: 400px;height: 420px;float: left;box-sizing: border-box;">
       <span v-for="song in songList" class="letter">
         <div v-if="showType=='按首字母' && song.letter == selectLetter" @click="changeSong(song)"  :class="song==selectSong?'selectSong':''">
           {{song.name}}
             <Link :to="song.number"> GO!</Link>
         </div>
         <div v-if="showType=='按顺序' && selectOrder && selectOrder.values.indexOf(song.number) >-1" @click="changeSong(song)"  :class="song==selectSong?'selectSong':''">
           {{song.name}}
             <Link :to="song.number"> GO!</Link>
         </div>
        </span>
    </span>
    <div v-if="selectSong" style="float: left;box-sizing: border-box;width: 50%;height: 420px;overflow-y: scroll;">
      <div style="padding: 20px;overflow-y: scroll;height: 420px">
        <div v-for="text in selectSong.texts" class="songText">
          {{text}}
        </div>
      </div>
    </div>
    <video  v-if="selectSong" id="video" :src="getMusicSrc(selectSong)"  width="260" height="40"
            controls
            style="filter:opacity(50%);position: absolute;right: 10px; bottom: 20px" :autoplay="false"
            :loop="$slidev.configs.musicPlayMode == 'loop'"
            webkit-playsinline playsinline x5-video-player-type="h5-page"
    >
      浏览器不支持播放音乐
    </video>
  </div>
</template>

<script>
import songlist from '/setup/songlist'

export default {
  name:'SongList',
  components:{
  },
  data() {
    return {
      showType: '按首字母',
      songList: songlist,
      letters: [],
      orders: [],
      selectLetter: 'A',
      selectOrder: null,
      selectSong: null,
      pageSize: 50
    }
  },
  mounted() {
    let num =[]
    this.songList.forEach(song=>{
      if(this.letters.indexOf(song.letter) <0){
        this.letters.push(song.letter)
      }
      num.push(song.number)
      if(num.length == this.pageSize || this.songList.indexOf(song) === this.songList.length-1){
        const order = {
          'name': num[0] + '-' + num[num.length-1],
          'values': num
        }
        if(this.pageSize == song.number){
          this.selectOrder = order
        }
        this.orders.push(order)
        num = []
      }
    })
  },
  methods: {
    getMusicSrc(selectSong){
      return import.meta.env.BASE_URL+ 'assets/media/' + selectSong.list[0]
    },
    changeLetter(letter){
      this.selectLetter = letter
    },
    changeOrder(order){
      this.selectOrder = order
    },
    changeSong(song){
      this.selectSong = song
    }
  }
}
</script>
<style>
.player-container{
  height: 200px;
  width: 200px;
}
span.verse-title{
  color: #f58529;
}
.selectLetter{
  color: #f58529;
  margin-right: 10px;
}
.selectSong{
  color: #f58529;
}
.letter{
  color: #FFFFFF;
  margin-right: 10px;
  text-align: left;
}
.songText{
  margin-bottom: 10px;
}
</style>
