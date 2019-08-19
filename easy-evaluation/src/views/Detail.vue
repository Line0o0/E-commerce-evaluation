<template>
  <div class="detail">
    <div class="content">
      <div class="content-left">
        <router-link to="./">
          <img class="image" :src="`${publicPath}xiaoxiong.png`" />
        </router-link>
        <p class="image-desc">点击图片返回主页</p>
      </div>
      <div class="content-right">
        <div class="brand">
          <input class="brand-input" v-model="brand" placeholder="请输入品牌名称" v-on:keyup.enter="onSubmitBrand" />
          <button class="brand-submit" v-on:click="onSubmitBrand">提 交</button>
        </div>
        <div class="link">
          <input class="link-input" v-model="link" placeholder="请输入商品链接" v-on:keyup.enter="onSubmitLink" />
          <button class="link-submit" v-on:click="onSubmitLink">提 交</button>
        </div>
        <div class="comment">
          <textarea class="comment-input" v-model="comment" placeholder="请输入商品评论"></textarea>
          <button class="comment-submit" v-on:click="onSubmitComment">提 交</button>
        </div>
      </div>
    </div>
    <div class="result" v-show="isShow === true">
      <h3 class="title">结 果 展 示</h3>
      <div class="container" v-show="isLoading === true">
        <p style="font-size: 24px;">正在针对您的输入进行数据分析，请稍候......</p>
        <img :src="`${publicPath}loading.gif`" />
      </div>
      <div class="container" v-show="isBrand === true">
        <div style="margin-bottom: 20px; margin-top: 20px;">
          <p style="font-size: 22px; font-weight: 500; margin-bottom: 35px;">共有 <span style="font-size: 30px; color: cornflowerblue">{{ brandResultTotalComment }}</span> 条顾客评论</p>
          <div style="width: 500px; height: 500px;" id="barchart4brand"></div>
          <div style="width: 500px; height: 500px;" id="piechart4brand"></div>
        </div>
      </div>
      <div class="container" v-show="isLink === true">
        <div class="link-result">
          <div style="margin-bottom: 20px; margin-top: 10px;">
            <p style="font-size: 22px; font-weight: 500; margin-bottom: 35px;">共爬取 <span style="font-size: 30px; color: #ffce00">{{ linkResultTotalComment }}</span> 条顾客评论，总评分为 <span style="font-size: 30px; color: #0066c0">{{ linkResultTotalStar }}</span> 星</p>
            <div class="progress-item" v-for="star in linkResultStars" :key="star['desc']">
              <div class="progress-item-title">{{ star['desc'] }}</div>
              <div class="progress-container"><div class="progress" :style="{ width: star['perc']+'%' }"></div></div>
              <div class="progress-item-percentage">{{ star['perc'] }}%</div>
            </div>
          </div>
          <div style="margin-bottom: 20px; margin-top: 20px;">
            <p style="font-size: 22px; font-weight: 500; margin-bottom: 35px;">以下是对评论进行分析后得出的结论</p>
            <div style="width: 500px; height: 500px;" id="barchart4link"></div>
            <div style="width: 500px; height: 500px;" id="piechart4link"></div>
          </div>
        </div>
      </div>
      <div class="container" v-show="isComment === true">
        <div class="comment-result">
          <div>
            <p style="font-size: 30px;">这 可 能 是 一 条 <span style="font-size: 40px; color: cornflowerblue;">{{ commentResultPolarity }}</span> 评 论 哦</p>
            <p style="font-size: 30px;">得 分 ：<span style="font-size: 40px; color: DeepPink;">{{ commentResultScore }}</span></p>
          </div>
          <img :src="`${publicPath}xiaomao.jpg`"/>
        </div>
      </div>
      <div class="container" v-show="isError === true">
        <p style="font-size: 30px; margin-bottom: 80px;">对 不 起 ，请 求 失 败 ，请 重 试</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import { setTimeout } from 'timers';
const echarts = require('echarts');
export default {
  name: 'detail',
  data: function () {
    return {
      publicPath: process.env.BASE_URL,
      brand: '',
      link: '',
      comment: '',
      isShow: false,
      isLoading: false,
      isBrand: false,
      isLink: false,
      isComment: false,
      isError: false,
      commentResultPolarity: '',
      commentResultScore: '',
      linkResultTotalComment: 0,
      linkResultTotalStar: 0,
      linkResultStars: [],
      brandResultTotalComment: 0
    }
  },
  methods: {
    drawBarChart: function (elemId, positiveNum, nagetiveNum) {//根据分析结果做出可观性强的柱形图
      echarts.init(
        document.getElementById(elemId)
      ).setOption({
        title: { text: '柱形图' },
        xAxis: {
          type: 'category',
          data: [
            {
              value: '好 评',
              textStyle: {
                align: 'center',
                color: 'DeepPink',
                shadowColor: 'rgba(0, 0, 0, 0.5)',
                fontSize: 18
              }
            },
            {
              value: '差 评',
              textStyle: {
                align: 'center',
                color: 'cornflowerblue',
                shadowColor: 'rgba(0, 0, 0, 0.5)',
                fontSize: 18
              }
            }]
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'bar',
          barWidth: '40%',
          itemStyle: {
            normal: {
              label: {
                show: true,
                textStyle: {
                  fontSize: 14
                }
              }
            }
          },
          data: [
            {
              value: positiveNum, 
              itemStyle: {
                color: 'DeepPink',
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            {
              value: nagetiveNum,
              itemStyle: {
                color: 'cornflowerblue',
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }]
        }]
      })
    },
    drawPieChart: function (elemId, positiveNum, nagetiveNum) {//根据分析结果作饼状图
      echarts.init(
        document.getElementById(elemId)
      ).setOption({
        title: { text: '饼状图' },
        legend: {
            data: [{
              name: '好评',
              icon: 'circle'
            },
            {
              name: '差评',
              icon: 'circle'
            }]
        },
        series: [{
          type: 'pie',
          radius: '60%',
          label: {
            normal: {
              show: true,
              position: 'inside',
              formatter: '{b} {d}%',
              textStyle: {
                fontSize: 20
              }
            }
          },
          data: [
              { value: positiveNum,
                name: '好 评',
                itemStyle: {
                  color: 'DeepPink',
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
              }},
              { value: nagetiveNum,
                name: '差 评',
                itemStyle: {
                  color: 'cornflowerblue',
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
              }}
          ]
        }]
      })
    },
    onShow: function (showed) {//控制下方结果展示板块的显示与隐藏
      if (showed === 'loading') {
        this.isLoading = true
        this.isBrand = false
        this.isLink = false
        this.isComment = false
        this.isError = false
      } else if (showed === 'brand') {
        this.isLoading = false
        this.isBrand = true
        this.isLink = false
        this.isComment = false
        this.isError = false
      } else if (showed === 'link') {
        this.isLoading = false
        this.isBrand = false
        this.isLink = true
        this.isComment = false
        this.isError = false
      } else if (showed === 'comment') {
        this.isLoading = false
        this.isBrand = false
        this.isLink = false
        this.isComment = true
        this.isError = false
      } else if (showed === 'error') {
        this.isLoading = false
        this.isBrand = false
        this.isLink = false
        this.isComment = false
        this.isError = true
      }
    },
    onSubmitBrand: function () {//输入品牌名称时的提交操作
      this.isShow = true
      window.scrollTo(0, 650)
      this.onShow('loading')
      // console.log(this.brand)
      let that = this
      let formData = {
          'brand': this.brand
      }
      axios({
        url: 'http://47.107.123.141/api/analyze_brand',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        // console.log(res)
        if (res.data.code === 'success') {
          that.onShow('brand')
          let positiveNum = res.data.positive_number
          let nagetiveNum = res.data.negative_number
          that.brandResultTotalComment = positiveNum + nagetiveNum
          that.drawBarChart('barchart4brand', positiveNum, nagetiveNum)
          that.drawPieChart('piechart4brand', positiveNum, nagetiveNum)
        } else { // res.data.code === 'failed'
          that.onShow('error')
          setTimeout(()=>{alert(res.data.message)},100)
        }
      }).catch(function (err) {
        console.log(err)
        that.onShow('error')
      })
    },
    onSubmitLink: function () {//输入商品链接时的提交操作
      this.isShow = true
      window.scrollTo(0, 650)
      this.onShow('loading')
      // console.log(this.link)
      let that = this
      let formData = {
          'link': this.link
      }
      axios({
        url: 'http://47.107.123.141/api/analyze_url',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        // console.log(res)
        if (res.data.code === 'success') {
          that.onShow('link')
          let positiveNum = res.data.positive_number
          let nagetiveNum = res.data.negative_number
          that.drawBarChart('barchart4link', positiveNum, nagetiveNum)
          that.drawPieChart('piechart4link', positiveNum, nagetiveNum)
          let stars = res.data.stars
          that.linkResultTotalComment = parseInt(stars[0])
          that.linkResultTotalStar = parseFloat(stars[1])
          that.linkResultStars = []
          that.linkResultStars.push({ 'desc': '5 星', 'perc': (stars[2] === null) ? 0 : parseInt(stars[2])})
          that.linkResultStars.push({ 'desc': '4 星', 'perc': (stars[3] === null) ? 0 : parseInt(stars[3])})
          that.linkResultStars.push({ 'desc': '3 星', 'perc': (stars[4] === null) ? 0 : parseInt(stars[4])})
          that.linkResultStars.push({ 'desc': '2 星', 'perc': (stars[5] === null) ? 0 : parseInt(stars[5])})
          that.linkResultStars.push({ 'desc': '1 星', 'perc': (stars[6] === null) ? 0 : parseInt(stars[6])})
        } else { // res.data.code === 'failed'
          that.onShow('error')
          setTimeout(()=>{alert(res.data.message)},100)
        }
      }).catch(function (err) {
        console.log(err)
        that.onShow('error')
      })
    },
    onSubmitComment: function () {//输入评论时的提交操作
      this.isShow = true
      window.scrollTo(0, 650)
      this.onShow('loading')
      // console.log(this.comment)
      let that = this
      let formData = {
          'comment': this.comment
      }
      axios({
        url: 'http://47.107.123.141/api/analyze_comment',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        // console.log(res)
        if (res.data.code === 'success') {
          that.onShow('comment')
          that.commentResultPolarity = (res.data.message === 'positive') ? '正 面' : '负 面'
          that.commentResultScore = res.data.score
        } else { // res.data.code === 'failed'
          that.onShow('error')
          setTimeout(()=>{alert(res.data.message)},100)
        }
      }).catch(function (err) {
        console.log(err)
        that.onShow('error')
      })
    }
  }
}
</script>

<style scoped lang="less">
.detail {
  height: 100%;
  width: 100%;
  margin: 50px 0;
  background: cornflowerblue;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content {
  width: 90%;
  height: 500px;
  margin-top: 50px;
  margin-bottom: 50px;
  border: 1px solid white;
  border-radius: 20px;
  background: white;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.8);
}

.content-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 2;
  margin-right: -5%;
}

.image {
  width: 90%;
  height: 90%;
}

.image-desc {
  color: grey;
  font-size: 14px;
  float: center;
  margin-top: -5%;
}

.content-right {
  height: 90%;
  width: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 3;
}

.brand {
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  margin-right: 2%;
  margin-bottom: 3%;
}

.brand-input {
  width: 90%;
  height: 90%;
  border: 1px solid rgba(96, 96, 96, 0.2);
  border-radius: 10px;
  background: LightCyan;
  opacity: 0.5;
  font-size: 100%;
  font-weight: 500;
  padding-left: 2%;
  padding-right: 2%;
  flex: 7;
  margin-right: 2%;
}

.brand-submit {
  width: 50%;
  height: 80%;
  border-radius: 10px;
  color: white;
  background: RGB(140,210,210);
  opacity: 0.5;
  font-weight: 700;
  font-size: 100%;
  flex: 1;
}

.brand-submit:hover {
  cursor: pointer;
  background-color: cornflowerblue;
}

.link {
  height: 10%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  margin-right: 2%;
  margin-bottom: 5%;
}

.link-input {
  width: 90%;
  height: 90%;
  border: 1px solid rgba(96, 96, 96, 0.2);
  border-radius: 10px;
  background: LightCyan;
  opacity: 0.5;
  font-size: 100%;
  font-weight: 500;
  padding-left: 2%;
  padding-right: 2%;
  flex: 7;
  margin-right: 2%;
}

.link-submit {
  width: 50%;
  height: 80%;
  border-radius: 10px;
  color: white;
  background: RGB(140,210,210);
  opacity: 0.5;
  font-weight: 700;
  font-size: 100%;
  flex: 1;
}

.link-submit:hover {
  cursor: pointer;
  background-color: cornflowerblue;
}

.comment {
  height: 50%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: flex-end;
  margin-right: 2%;
}

.comment-input {
  width: 90%;
  height: 90%;
  padding: 2px;
  border: 1px solid rgba(96, 96, 96, 0.2);
  border-radius: 15px;
  background: LightCyan;
  opacity: 0.5;
  font-size: 120%;
  font-weight: 500;
  padding: 2%;
  flex: 7;
  margin-right: 2%;
}

.comment-submit {
  width: 50%;
  height: 16%;
  border-radius: 10px;
  color: white;
  background: RGB(140,210,210);
  opacity: 0.5;
  font-weight: 700;
  font-size: 100%;
  flex: 1;
}

.comment-submit:hover {
  cursor: pointer;
  background-color: cornflowerblue;
}

.result {
  width: 90%;
  margin-bottom: 50px;
  border: 1px solid white;
  border-radius: 20px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.8);
}

.title {
  font-size: 50px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.link-result {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.comment-result {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.progress-container {
  width: 400px;
  height: 20px;
  background-color: #f3f3f3;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.4);
}

.progress {
  height:20px;
  background-color: #ffce00;
}

.progress-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.progress-item-title {
  font-weight: 500;
  font-size: 18px;
  color: #0066c0;
  margin-right: 20px;
}

.progress-item-percentage {
  font-weight: 500;
  font-size: 15px;
  color: #555;
  margin-left: 12px;
  width: 5px;
}

.b {
  color:#fff;
  font-weight: 100;
  font-size: 12px;
}

</style>
