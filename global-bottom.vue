<!-- global-top.vue -->
<template>
  <footer class="absolute bottom-10 right-0 right-0 p-2" style="z-index: 1">
    <video v-show="getMusic($slidev.nav.currentPage) && $slidev.configs.showmusic" id="video"
           :src="$slidev.configs.showmusic?getMusic($slidev.nav.currentPage):''" width="300" height="100"
           controls
           style="filter:opacity(50%)" :autoplay="$slidev.configs.showmusic"
           :loop="$slidev.configs.musicPlayMode == 'loop'"
           webkit-playsinline playsinline x5-video-player-type="h5-page"
    >
      <!--      <track kind="subtitles" src="/assets/vtt/test.vtt" srclang="zh-cn" label="Chinese">-->
      浏览器不支持播放音乐
    </video>
    <Link id="music_go" :to="getMusicId($slidev.configs.musicPlayMode)" title="">
    </Link>
    <!--    BFC-->
  </footer>
  <footer class="drawer absolute bottom-10 right-0 right-0 p-2" style="z-index: 1">
    <div class="setbox" :class="{show: $slidev.configs.isshow}">
      <div>
        <button class="icon-btn scripture" :class="oldnew == 'old'?'btn-selected':''" @click="changeOldNew('old')"
                border="~ white-400 opacity-50 rounded-md">
          旧约
        </button>
        <button class="icon-btn scripture" :class="oldnew == 'new'?'btn-selected':''" @click="changeOldNew('new')"
                border="~ white-400 opacity-50 rounded-md">
          新约
        </button>
      </div>
      <div v-if="scriptureList.length >0">
        <div class="el-divider el-divider--horizontal">
          <div class="el-divider__text is-left">经文</div>
        </div>
        <span v-for="scripture in scriptureList">
             <button class="icon-btn scripture" :class="selectedScriptureId == scripture.id?'btn-selected':''"
                     v-if="scripture.oldnew === oldnew" @click="selectScripture(scripture.id, scripture.chapters)"
                     border="~ white-400 opacity-50 rounded-md">
              {{ scripture.name_cn }}
            </button>
        </span>
      </div>
      <div v-if="chapterList.length >0">
        <div class="el-divider el-divider--horizontal">
          <div class="el-divider__text is-left">章</div>
        </div>
        <span v-for="chapter in chapterList">
             <button class="icon-btn scripture" :class="selectedChapter == chapter?'btn-selected':''"
                     @click="selectChapter(chapter)"
                     border="~ white-400 opacity-50 rounded-md">
              {{ chapter }}
            </button>
        </span>
      </div>
      <div v-if="verseList.length >0">
        <div class="el-divider el-divider--horizontal">
          <div class="el-divider__text is-left">节</div>
        </div>
        <span v-for="verse in verseList">
             <button class="icon-btn scripture"
                     :class="(verse.verse ==start)||(verse.verse >=start && verse.verse <=end)?'btn-selected':''"
                     @click="selectVerse(verse)"
                     border="~ white-400 opacity-50 rounded-md">
              {{ verse.verse }}
            </button>
        </span>
        <button class="icon-btn scripture" @click="resetStartAndEnd()"
                border="~ white-400 opacity-50 rounded-md">
          取消
        </button>
        <button class="icon-btn scripture"
                @click="$slidev.configs.isshow=false;$slidev.configs.selectedVerseList=getSelectedVerseList()"
                border="~ white-400 opacity-50 rounded-md">
          确定
        </button>
      </div>
    </div>
  </footer>
</template>

<script>
import initSqlJs from "sql.js"
// Required to let webpack 4 know it needs to copy the wasm file to our assets
// import sqlWasm from "!!file-loader?name=sql-wasm-[contenthash].wasm!sql.js/dist/sql-wasm.wasm";
import _Broadcast from '/setup/Broadcast/lib'

export default {
  name: 'sql',
  data() {
    return {
      listener: null,
      isshow: false,
      DB: null,
      scriptureList: [], // 目录
      chapterList: [], //章
      verseList: [], //节
      oldnew: 'old', //old，new 旧约 新约
      selectScriptureList: [],
      selectedScriptureId: 1,
      selectedChapter: 1,
      selectedVerseList: [],
      start: undefined,
      end: undefined,
      currentMusicId: 1,
      musicMap: {
        81: ['081我要弹琴歌唱赞美你.mp3'],
        178: ['178-.mp3'],
        251: ['251-.mp3', '251-看.mp3'],
        208: ['208-耶和华我的磐石.mp3'],
        5: ['005宝贵十架.mp3', '005宝贵十架韩文.mp3'],
        139: ['139-.mp3'],
        93: ['093-.mp3', '093-献.mp3'],
        55: ['055-奇.mp3', '055奇异恩典_女声.mp3', '055-英.mp3', '055-流行唱法.mp3'],
        210: ['210-.mp3'],
        142: ['142-.mp3'],
        62: ['062使命.mp3'],
        257: ['257-圣哉圣哉圣哉.mp3'],
        115: ['115-.mp3'],
        45: ['045来庆贺.mp3'],
        181: ['181-（伴奏）.mp3'],
        201: ['201-这里有荣耀.mp3'],
        265: ['265-只愿得着你.mp3'],
        52: ['052全新的你.mp3'],
        140: ['140众山怎样围绕耶路撒冷.mp3'],
        154: ['154-.mp3'],
        36: ['036.和散那.mp3'],
        306: ['306更深经历你.mp3'],
        57: ['057人的生命只有一次.mp3'],
        9: ['009不知道前方的路还有多远版本二.mp3', '009不知道前方的路还有多远.mp3'],
        145: ['145 主的怜悯已降临.mp3', '145我们一起祷告吧_合唱.mp3'],
        218: ['218-耶和华神已掌权.mp3'],
        162: ['162主啊，差遣我.mp3'],
        53: ['053轻轻听.mp3'],
        174: ['174-你.mp3'],
        4: ['004阿爸父.mp3'],
        61: ['061认识你真好.mp3'],
        200: ['200看见神的爱.mp3'],
        74: ['074我的救赎者活着.mp3'],
        230: ['230-.mp3'],
        179: ['179尽心尽力赞美主_现场.mp3'],
        119: ['119-.mp3'],
        226: ['226-.mp3'],
        273: ['273一粒麦子.mp3'],
        40: ['040.经过主宝血.mp3'],
        122: ['122主使软弱变刚强_通俗女.mp3'],
        158: ['158-.mp3'],
        202: ['202.耶稣耶稣我要赞美你.mp3'],
        159: ['159-.mp3'],
        224: ['224主啊陶造我.mp3'],
        138: ['138中国早晨五点钟_美声女.mp3'],
        227: ['227-.mp3'],
        118: ['118-.mp3', '118-主.mp3'],
        231: ['231-.mp3'],
        67: ['067神啊！我要赞美你.mp3'],
        249: ['249我的神我的父我的磐石_瑕疵.mp3', '249-.mp3'],
        283: ['283.Jesus.mp3'],
        163: ['163-.mp3'],
        261: ['261求你国度降临.mp3'],
        17: ['017常常喜乐.mp3', '017-.mp3'],
        175: ['175-.mp3'],
        30: ['030-.mp3', '030感恩的泪_女声.mp3'],
        176: ['176以便以谢的神_现场.mp3'],
        244: ['244耶和华果然成就大事.mp3'],
        295: ['295因祂活着(3段).mp3', '295因祂活着.mp3'],
        76: ['076.我的至爱我的生命-伴奏.mp3'],
        155: ['155-.mp3'],
        143: ['143神羔羊_女声.mp3'],
        315: ['315主说你能.mp3'],
        56: ['056-起.mp3', '056起来吧_女声_美声.mp3'],
        72: ['072我的心你要称颂耶和华-伴奏.mp3'],
        289: ['289陪我走过春夏秋冬.mp3'],
        114: ['114-.mp3'],
        299: ['299我不为自己活.mp3'],
        1: ['001_.mp3', '001爱.mp3'],
        211: ['211-.mp3'],
        92: ['092-.mp3'],
        239: ['239-不要怕.mp3'],
        246: ['246-.mp3', '246-敬.mp3'],
        297: ['297我愿触动你心弦.mp3'],
        180: ['180-.mp3'],
        3: ['003爱 喜乐 生命.mp3'],
        196: ['196-.mp3'],
        161: ['161.向我主唱哈利路亚.mp3'],
        225: ['225-这世代.mp3'],
        207: ['207-.mp3'],
        95: ['095-伴奏.mp3'],
        259: ['259-敬拜赞美迎来神同在.mp3'],
        123: ['123主再来到这世界为止韩文.mp3', '123主再来到这世界为止.mp3'],
        172: ['172-.mp3'],
        20: ['020-曾有一双手.mp3', '020-.mp3'],
        133: ['133-.mp3'],
        236: ['236-.mp3'],
        260: ['260-能不能(纯音乐).mp3'],
        109: ['109-.mp3'],
        79: ['079我有平安如江河_二个.mp3'],
        243: ['243你们要先求他的国.mp3'],
        83: ['083-.mp3'],
        129: ['129-.mp3'],
        49: ['049你们要赞美耶和华_欢快.mp3', '049你们要赞美耶和华.mp3', '049-.mp3'],
        128: ['128在主爱中.mp3'],
        168: ['168-.mp3'],
        187: ['187-.mp3'],
        310: ['310主你本为大.mp3'],
        19: ['019-赐我自由.mp3', '019-.mp3'],
        60: ['060-男声.mp3', '060荣耀归主名_女声.mp3'],
        113: ['113-.mp3'],
        105: ['105-.mp3'],
        100: ['100.耶稣爱我万不错.mp3'],
        132: ['132在他没有难成的事.mp3'],
        12: ['012差遣之歌男声.mp3', '012差遣之歌_女声.mp3'],
        152: ['152-.mp3'],
        258: ['258-祢是我的一切.mp3'],
        54: ['054.倾听我的心.mp3'],
        73: ['073我的神我敬拜你.mp3', '073-我.mp3'],
        16: ['016-.mp3', '016.mp3'],
        22: ['022当以感谢进入他的门_合唱.mp3'],
        280: ['280主，我邀请你.mp3'],
        43: ['043.欢乐颂.mp3'],
        104: ['104-.mp3'],
        47: ['047.每一天所度过的每一刻.mp3'],
        97: ['097兴起为耶稣_合唱.mp3'],
        121: ['121最知心的朋友合唱.mp3', '121最知心的朋友美声.mp3'],
        112: ['112-.mp3'],
        24: ['024得胜得胜_童声.mp3'],
        88: ['088-唯.mp3'],
        7: ['007别怕路艰难发哥.mp3', '007别怕路艰难.mp3'],
        14: ['014把冷漠变成爱.mp3'],
        217: ['217-.mp3'],
        94: ['094-.mp3'],
        130: ['130.赞美从心而出.mp3'],
        240: ['240-.mp3'],
        309: ['309天父美善力量.mp3'],
        169: ['169-.mp3'],
        186: ['186-.mp3', '186我们是光明之子_快.mp3'],
        51: ['051全然向你.mp3'],
        44: ['044空谷的回音_女声.mp3'],
        314: ['314耶和华以勒我的主.mp3'],
        87: ['087.mp3'],
        68: ['068田地里的庄稼.mp3'],
        82: ['082-.mp3'],
        144: ['144 我们一起祷告吧合唱.mp3'],
        166: ['166耶和华喜乐灵.mp3'],
        103: ['103-伴奏.mp3'],
        221: ['221-.mp3'],
        302: ['302你爱我到底.mp3'],
        58: ['058让赞美飞扬.mp3'],
        99: ['099.虚心的人有福了.mp3'],
        11: ['011唱一首天上的歌合唱.mp3', '011唱一首天上的歌.mp3'],
        237: ['237-.mp3', '237-愿.mp3'],
        292: ['292普世欢腾歌.mp3'],
        157: ['157求你吸引我来到十架前_伴奏.mp3'],
        34: ['034.我们高举双手赞美主.mp3'],
        149: ['149-.mp3'],
        305: ['305每一次我赞美主.mp3'],
        59: ['059如鹿渴慕溪水_合唱.mp3'],
        148: ['148.将这山地赏赐给我们.mp3'],
        98: ['098-.mp3'],
        250: ['250我主尊荣可畏.mp3'],
        301: ['301.神是看顾我的神.mp3'],
        199: ['199奇妙神迹.mp3'],
        165: ['165-.mp3'],
        147: ['147十字架的道路殉道者的生命_伴奏.mp3'],
        298: ['298抬起我的头.mp3'],
        296: ['296我知谁掌管明天(原本).mp3', '296我知谁掌管明天.mp3'],
        23: ['023向耶和华歌唱_合唱_卡农.mp3'],
        39: ['039.哈利路！主我神作王了.mp3'],
        124: ['124-.mp3'],
        277: ['277标竿人生路.mp3'],
        234: ['234我要来敬拜你，主.mp3'],
        222: ['222-.mp3'],
        32: ['032_.mp3'],
        13: ['013彩虹下的约定2.mp3', '013彩虹下的约定1.mp3'],
        303: ['303恩典.mp3'],
        268: ['268耶稣是主.mp3'],
        241: ['241谨慎自守_男声_吉他.mp3'],
        213: ['213Hi-Ne-Ni（我在这里）_大合唱_不佳.mp3', '213-.mp3'],
        135: ['135这一生最美的祝福合唱.mp3', '135这一生最美的祝福.mp3'],
        131: ['131-.mp3'],
        117: ['117-应.mp3'],
        189: ['189-.mp3', '189主耶稣被钉在十架上_现场.mp3'],
        290: ['290牵我的手.mp3'],
        101: ['101耶和华是爱.mp3'],
        170: ['170-.mp3'],
        274: ['274我有一个荣美家乡(伴奏).mp3'],
        287: ['287恳求主使用我们.mp3'],
        150: ['150-.mp3'],
        8: ['008不是没有家.mp3'],
        15: ['015-.mp3', '015从太阳出来之地_和声.mp3'],
        263: ['263-注目看耶稣.mp3'],
        212: ['212.赞美耶稣歌.mp3'],
        107: ['107-.mp3'],
        220: ['220-十字架的传达者.mp3'],
        153: ['153.愿你荣耀过度降临.mp3'],
        238: ['238-.mp3'],
        245: ['245天地的颂赞.mp3'],
        50: ['050.磐石磐石耶稣基督.mp3'],
        232: ['232以色列兴起.mp3'],
        214: ['214-.mp3'],
        78: ['078-.mp3', '078我以祷告来到你跟前.mp3'],
        184: ['184是此刻是现在_现场.mp3'],
        288: ['288盟约.mp3'],
        271: ['271展开属天的翅膀.mp3'],
        185: ['185-.mp3'],
        193: ['193-.mp3'],
        228: ['228.我敬拜你全能真神.mp3'],
        66: ['066-神.mp3', '066神真是我力量.mp3'],
        308: ['308从亘古到永远.mp3'],
        216: ['216亲眼看见你.mp3'],
        65: ['065十字架的爱_女声.mp3'],
        312: ['312恳求圣灵降临.mp3'],
        38: ['038-.mp3', '038和过去不一样.mp3'],
        300: ['300高山低谷都赞美.mp3'],
        192: ['192-.mp3'],
        146: ['146-你.mp3'],
        96: ['096-.mp3'],
        291: ['291新生王歌.mp3'],
        215: ['215-.mp3'],
        110: ['110-.mp3'],
        248: ['248-仰望神的人.mp3', '248仰望神的人_合唱.mp3'],
        106: ['106-.mp3'],
        304: ['304他又真又活.mp3', '304祂又真又活.mp3'],
        282: ['282凡事都有神的美意.mp3'],
        279: ['279我愿为你去.mp3'],
        151: ['151-.mp3'],
        256: ['256-愿你吸引我.mp3'],
        173: ['173我歌，我主_音质不佳.mp3'],
        167: ['167-版本二.mp3'],
        126: ['126-.mp3'],
        171: ['171-.mp3'],
        164: ['164哈利路亚赞美主.mp3'],
        266: ['266谁能使我与神的爱隔绝.mp3'],
        281: ['281你们要赞美耶和华.mp3'],
        188: ['188-.mp3'],
        69: ['069弹琴歌唱赞美你.mp3', '069-.mp3'],
        276: ['276哈利路亚(你真奇妙).mp3'],
        85: ['085.我相信.mp3'],
        255: ['255-弟兄和睦同居.mp3'],
        294: ['294摩西的歌.mp3'],
        2: ['002爱 我愿意.mp3'],
        235: ['235-.mp3'],
        71: ['071同路人.mp3'],
        254: ['254-一道江河.mp3'],
        223: ['223-.mp3'],
        275: ['275恩典的记号.mp3'],
        86: ['086.为爱而生.mp3'],
        272: ['272-荣耀的呼召(伴奏).mp3'],
        70: ['070天堂在我心.mp3', '070-天.mp3'],
        64: ['064生命的执着.mp3'],
        21: ['021.当圣灵在我的心.mp3'],
        311: ['311复兴从我开始.mp3'],
        10: ['010唱哈利路亚.mp3'],
        160: ['160你就是耶稣-feat.陈萍.mp3', '160你就是耶稣.mp3'],
        267: ['267我属主.mp3'],
        108: ['108耶稣!耶稣!_摇滚.mp3'],
        91: ['091-.mp3'],
        183: ['183-.mp3'],
        29: ['029-.mp3'],
        264: ['264-到神的祭坛.mp3'],
        206: ['206主耶稣我爱你.mp3'],
        293: ['293荣耀歌.mp3'],
        204: ['204-.mp3'],
        278: ['278祢的恩典.mp3', '278你的恩典.mp3'],
        286: ['286安静.mp3'],
        75: ['075.我的心啊我的灵啊.mp3'],
        80: ['080我对祢的爱永不变.mp3'],
        252: ['252今生跟随主耶稣.mp3'],
        262: ['262你爱永不变-巫启贤.mp3'],
        194: ['194-求主充满我.mp3'],
        25: ['025-.mp3'],
        307: ['307我主何等伟大.mp3'],
        111: ['111.耶稣全得胜.mp3'],
        46: ['046每当我想起你.mp3'],
        219: ['219神同在.mp3'],
        209: ['209-.mp3'],
        313: ['313大海中的船.mp3'],
        269: ['269领我到你宝血里面.mp3'],
        77: ['077.我们又在一起.mp3'],
        120: ['120-.mp3'],
        198: ['198-.mp3'],
        177: ['177-.mp3'],
        48: ['048你是荣耀的君王.mp3'],
        63: ['063神的应许歌.mp3'],
        28: ['028复兴2000.mp3'],
        35: ['035活石.mp3'],
        33: ['033给我一颗中国心_庄严_颂诗.mp3'],
        242: ['242耶和华的心.mp3'],
        42: ['042十字架_女声_美声.mp3'],
        102: ['102-伴奏.mp3'],
        253: ['253-我心切切渴慕你.mp3'],
        90: ['90无声的赞美_女声.mp3'],
        233: ['233-.mp3'],
        247: ['247最美的礼物.mp3'],
        270: ['270耶稣基督是主.mp3'],
        127: ['127主啊我赞美你.mp3'],
        191: ['191-赞美耶稣.mp3'],
        137: ['137这里有神的同在.mp3'],
        41: ['041.就在那加利利海边.mp3'],
        205: ['205-.mp3', '205你真伟大_美声女.mp3'],
        195: ['195.齐来赞美.mp3'],
        182: ['182-.mp3'],
        197: ['197有一件礼物_女声.mp3'],
        31: ['031光明之子.mp3'],
        190: ['190.主啊！我要全心来敬拜你（伴奏）.mp3'],
        116: ['116-.mp3'],
        26: ['026丰盛的人生_女声.mp3'],
        125: ['125主啊,我到你面前.mp3'],
        229: ['229-.mp3'],
        156: ['156.祝福中国（多语版）.mp3'],
        285: ['285爱使我们相聚在一起.mp3'],
        136: ['136这信心啊！坚强起来.mp3']
      }
    }
  },
  watch: {},
  mounted() {
    console.log('env', JSON.stringify(import.meta.env))
    this.loadDB().then(db => {
      this.getScriptures()
    })
    const video = document.getElementById('video')
    // video.textTracks[0].mode ='showing'; //默认显示字幕
// 15、ended：播放结束
    video.addEventListener('ended', function (e) {
      console.log('视频播放完了')
      console.log(e)
      var btn_music_go = document.getElementById('music_go')
      btn_music_go.click()
    })
  },
  methods: {
    getMusicId(playMode) {
      if (playMode == 'loop') {
        return this.currentMusicId
      }
      const keys = Object.keys(this.musicMap)
      if (playMode == 'random') { //随机
        const musicId = keys[Math.floor((Math.random() * keys.length))];
        return musicId
      } else if (playMode == 'order') { //顺序
        if (this.currentMusicId == keys.length) {
          return 1
        }
        let musicId = this.currentMusicId + 1
        while (this.musicMap[musicId] == undefined) {
          musicId++;
        }
        return musicId
      }
      //replay
      return this.currentMusicId
    },
    getMusic(page) {
      let srcs = []
      if (this.musicMap[page]) {
        this.currentMusicId = page
        for (let i = 0; i < this.musicMap[page].length; i++) {
          const src = (import.meta.env.VITE_MP3_BASE_URL + 'assets/media/' + this.musicMap[page][i])
          console.log(src)
          srcs.push(src)
        }
      }
      console.log(srcs)
      return srcs[0]
    },
    close() {
      this.isshow = false
    },
    open() {
      this.isshow = true
    },
    changeOldNew(oldnew) {
      this.oldnew = oldnew
    },
    runQuery(sql, params) {
      let stmt = this.DB.prepare(sql);
      if (params) {
        stmt.getAsObject(params); // {col1:1, col2:111}
      }
      let results = []
      while (stmt.step()) { //
        let row = stmt.getAsObject();
        results.push(row)
      }
      return results
    },
    async loadDB() {
      try {
        // 这里加载的文件要前面要加 "/"
        const sqlPromise = await initSqlJs({
          // locateFile: () => sqlWasm
          // locateFile: filename => '/' + `${filename}`
          locateFile: filename => import.meta.env.BASE_URL + `assets/sql.js/${filename}`
          // locateFile: file => `https://sql.js.org/dist/${file}`
        });

        // 这里加载的文件要前面要加 "/"
        const dataPromise = fetch(import.meta.env.BASE_URL + "assets/bible.sqlite").then(res => res.arrayBuffer());
        const [SQL, buf] = await Promise.all([sqlPromise, dataPromise])
        const db = new SQL.Database(new Uint8Array(buf));
        this.DB = db
        return db
      } catch (err) {
        console.log(err);
      }
    },
    //经文目录
    getScriptures() {
      this.scriptureList = this.runQuery("SELECT * from scriptures where version=1 order by `order`")
      this.resetStartAndEnd()
    },
    selectScripture(selectedScriptureId, chapters) {
      console.log(selectedScriptureId, chapters)
      this.selectedScriptureId = selectedScriptureId
      this.chapterList = []
      for (let i = 1; i <= chapters; i++) {
        this.chapterList.push(i)
      }
      this.resetStartAndEnd()
      this.resetVerseList()
    },
    selectChapter(chapter) {
      console.log(this.selectedScriptureId, chapter)
      this.selectedChapter = chapter
      const sql = "SELECT * from verses where scripture = " + this.selectedScriptureId + " and chapter = " + chapter + " and version=1 order by verse asc"
      console.log(sql)
      this.verseList = this.runQuery(sql)
      this.resetStartAndEnd()
    },
    selectVerse(verse) {
      console.table(verse)
      if (this.start == verse.verse) {
        this.start = undefined
        this.end = undefined
        return
      }
      if (this.start == undefined) {
        this.start = verse.verse
      } else {
        this.end = verse.verse
        if (this.end < this.start) {
          let tmp = this.end
          this.end = this.start
          this.start = tmp
        }
      }
      console.log("start" + this.start)
      console.log("end" + this.end)
    },
    resetStartAndEnd() {
      this.start = undefined
      this.end = undefined
    },
    resetVerseList() {
      this.verseList = []
    },
    getSelectedVerseList() {
      this.selectedVerseList = []
      if (this.start == undefined) {
        this.start = 1
      }
      if (this.end == undefined) {
        this.end = this.verseList.length
      }
      for (let i = this.start; i <= this.end; i++) {
        this.selectedVerseList.push(this.verseList[i - 1])
      }
      console.log("start",this.start,"end", this.end)
      console.log(this.selectedVerseList)
      this.sendBroadcast()
      return this.selectedVerseList
    },
    sendBroadcast() {
      _Broadcast.$emit('VerseList', JSON.stringify(this.selectedVerseList))
    }
  }
}
</script>
<style lang="scss" scoped>
.drawer {
  //height: 500px;
  //width:100%;
  opacity: 0.7;
  display: flex;
  display: -webkit-flex;
  flex-direction: column;

  .setbox {
    overflow: scroll;
    position: fixed;
    z-index: 1000;
    top: 0px;
    bottom: 0px;
    width: 340px;
    height: 100%;
    background: #000000;
    border-left: 1px solid #CFD8DC !important;
    box-shadow: 0px 3px 12px rgba(0, 0, 0, 0.12);
    -webkit-transition: all 0.3s ease;
    transition: all 0.3s ease;
    right: -460px;
    padding: 5px 10px 5px 10px;
  }

  .show {
    right: 0;
  }

  .scripture {
    padding: 2px;
    margin: 2px;
    font-size: 5px;
    color: white;
  }

  .btn-selected {
    background-color: #FFFFFF;
    color: #000000;
  }
}
</style>