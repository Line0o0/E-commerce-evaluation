<template>
    <div class="contact">
        <div class="row" id="contactWithUs">
          <div>
            <router-link to="./">
            <img style="height:400px;text-indent: 20px;" src="../assets/timg.jpg">
            <p style="color:grey; font-size:14px;text-decoration:none; float:center;">点击图片返回主页</p>
            </router-link>
          </div>
          <div id="bugForm">
            <div style="text-align:center;line-height:0.5;">
              <h3>联系我们</h3>
              <h4>Contact With Us</h4>
              <p style="font-weight: bold;">请填写信息:</p>
            </div>
            <form style="text-align:left;">
              <label for="bug">问题反馈</label><br>
              <textarea id="Bug" placeholder="请描述你的问题" v-model="problem"></textarea><br>
              <label for="phone">联系邮箱</label><br>
              <input type="email" id="mailbox" placeholder="请输入你的邮箱" v-model="conMail"><br>
              <a id="sendmail" @click="submitBug()">提交</a>
            </form>
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
export default{
  name: 'contact',
  date: function(){
    return {
      problem: '',
      conMail: '',
    }
  },
  watch: {//监控各变量的变化
    problem: function (val) {
      this.problem = val
    },
    conMail: function (val) {
      this.conMail = val
    }
  },
  methods:{
    submitBug: function () {//将用户反馈的信息提交
      console.log(this.problem)
      console.log(this.conMail)
      let formData = {
        'problem': this.problem,
        'conMail': this.conMail
      }
      axios({
        url: 'http://47.107.123.141/api/contact',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        console.log(res.data)
        alert(res.data.message)
      }).catch(function (err) {
        console.log(err)
        alert(err)
      })
    }
  }
}
</script>

<style scoped lang="less">
  .contact{
    height: 100%;
    width: 100%;
    margin:50px 0;
    background: cornflowerblue;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .row{
    -webkit-column-count: 2; /* Chrome, Safari, Opera */
    -moz-column-count: 2; /* Firefox */
    column-count: 2;
    padding:20px;
  }
  #contactWithUs{
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
    box-shadow:0px 8px 16px 0px rgba(0,0,0,0.8);
  }
  #bugForm{
    border:3px solid lightblue;
    border-radius:10px;
    background-color:white;
    padding:30px;
    width:80%;
    font-size:18px;
  }
  #bugForm input[type=text], input[type=email],textarea {
    width:100%;
    padding: 6px;
    border: 1px solid #ccc;
    border-radius:10px;
    margin-top: 8px;
    margin-bottom: 16px;
    resize: vertical;
  }
  #Bug{
      height:80px;
      text-align:left;
      line-height:1;
      font-size:16px;
  }
  #mailbox{
      height:40px;
  }
  #bugForm a{
    background-color: rgb(128, 167, 240);
    border-radius:10px;
    width:100%;
    color: white;
    text-decoration:none;
    padding: 12px 20px;
    border: none;
    cursor: pointer;
  }
  #bugForm a:hover {
    background-color:cornflowerblue;
  }
</style>
