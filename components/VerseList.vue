<template>
  <div class="content">
    <div v-if="verseLists.length>0">
      <div v-for="(verseList,page) in verseLists" :key="'verse' + page">
        <div v-if="page==0">
          <div v-if="$slidev.nav.clicks ==page">
            <div v-if="verseList.length>0">
              <div v-for="item in verseList" class="verse-content">
                <span class="verse-title">{{item.scripture_cn}}{{item.chapter}}:{{item.verse}}</span>{{item.content}}
              </div>
            </div>
          </div>
        </div>
        <div v-else  v-click>
          <div v-if="$slidev.nav.clicks ==page">
            <div v-if="verseList.length>0">
              <div v-for="item in verseList" class="verse-content">
                <span class="verse-title">{{item.scripture_cn}}{{item.chapter}}:{{item.verse}}</span>{{item.content}}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else style="text-align: center">
      <button class="icon-btn" @click="$slidev.configs.isshow = !$slidev.configs.isshow">
        <carbon-awake />
      </button>
    </div>
  </div>
</template>

<script>
import _Broadcast from '/setup/Broadcast/lib'

export default {
  name:'VerseList',
  components:{
  },
  data() {
    return {
      selectedVerseList: [],
      verseLists:[],
      pageSize: 5
    }
  },
  mounted() {
    this.CreateListener()
  },
  methods: {
    // 注册订阅
    CreateListener() {
      console.log('我是订阅者A，我订阅的主题是VerseList')
      this.listener = _Broadcast.$on('VerseList', (type, value) => {
        this.selectedVerseList = JSON.parse(type)
        this.verseLists = []
        let verseList = []
        for (let i = 0; i < this.selectedVerseList.length; i++) {
          verseList.push(this.selectedVerseList[i])
          if(verseList.length % this.pageSize==0){
            this.verseLists.push(verseList)
            verseList = []
          }
        }
        if(verseList.length>0){
          this.verseLists.push(verseList)
        }
        console.log("verseLists",this.verseLists)
      })
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
.verse-content{
  line-height: 1;
}
</style>
