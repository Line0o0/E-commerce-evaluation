<template>
    <div class="home">
     <!--*****************************************动态背景**********************************-->
     <!--***************************************首页上半部分********************************-->
      <div id="header">
        <div id="logo" style="text-align:center;width:20%;padding:15px;">
          <img alt="Our logo" src="../assets/logo.png" style="width:30%;height:20%;"/>
        </div>
        <div id="menu">
          <a href="#homeContent">首页</a>
          <a @click="toPage('./Detail')">评价分析</a>
          <a @click="toPage('./Contact')">联系我们</a>
          <a id="signup" style="float: right;" @click="showDiv('forSignUp')">注册</a>
          <a id="login" style="float: right;" @click="showDiv('forSignIn')">登录</a>
          <a id="logout" style="float: right; display:none;" @click="logOut()">退出</a>
        </div>
      </div>
     <!--***************************************首页下半部分********************************-->
      <div id="homeContent">
        <div class="picShow">
          <v-slider></v-slider>
        </div>
        <img src="../assets/intro.jpg" style="height: 400px; overflow: hidden; width: 40%; margin-left: 3%;">
        <!--
        <div class="intro">
          <h2 style="color:cornflowerblue">应用简介</h2><br/>
          <p>移动支付的广泛应用使得电商在最近几年已经成为很多用户购物的首选</p>
          <p>用户在进行网购的时候大多会有查看评价区的习惯，以判断商品是否值得购买</p>
          <p>但在面对<b>繁多</b>的用户评价时，用户需要一条一条的查看后作出判断显然不是很方便</p>
          <p>因此，我们这款软件将对每一条评论进行<b>情感分析</b>后判断是好评还是差评</p>
          <p>然后将统计结果进行<b>可视化展出</b>，那么将给用户的选择带来很大的便利</p>
          <p style="color:cornflowerblue">用户只需要登录账号,输入批量商品评论或商品链接</p>
          <p style="color:cornflowerblue">等待一定时间，即可看到智能分析结果</p>
        </div>
        -->
      </div>
      <div style="width:100%; float:left; overflow:hidden;">
        <img src="../assets/timg.gif" style="width:20%;">
        <img src="../assets/timg.gif" style="width:20%;">
        <img src="../assets/timg.gif" style="width:20%;">
        <img src="../assets/timg.gif" style="width:20%;">
        <img src="../assets/timg.gif" style="width:20%;">
      </div>
     <!--***************************************注册登录部分********************************-->
      <div id="bg_div" class="bg_shadow" @click="hideDiv()"></div>
      <div id="forSignIn" class="div_content" style="line-height:1;width:auto;height:auto;">
        <div style="text-align:center;font-size:28px; line-height:20%;">
          <p>登录</p>
          <p style="font-family:monospace;font-style:italic;">Sign In</p>
        </div>
        <input type="text" name="user_id" placeholder="用户名" v-model="userID" required><br>
        <input type="password" name="pwd" placeholder="密码" v-model="rePWD" @keyup.enter="signIn()" required><br><br>
        <input type="checkbox" id="remInfo" style="float:left;" v-model="remember">
        <label for="remInfo" style="float:left;">记住密码</label>
        <label for="autoSignIn" style="float:right;">自动登录</label>
        <input type="checkbox" id="autoSignIn" v-model="autoS" style="float:right;"><br>
        <button style="font-size:24px;" @click="signIn()">登录</button><br><br>
        <span style="float: left;color:blue;font-weight:800;cursor:pointer;" @click="changeView('forSignIn','forSignUp')">新用户注册</span>
        <span style="float: right;color:rgb(161, 159, 159);cursor:pointer;" @click="changeView('forSignIn','forReset')">忘记密码</span>
      </div>
      <div id="forSignUp" class="div_content">
        <div style="text-align:center;font-size:28px; line-height:20%;">
          <p>注册</p>
          <p style="font-family:monospace;font-style:italic;">Sign Up</p>
        </div>
        <input type="text" name="user_name" placeholder="用户名" v-model="userID" required><br>
        <input type="password" name="pwd" placeholder="密码" v-model="userPwd" required><br>
        <input type="password" name="ensurePwd" placeholder="确认密码" v-model="rePWD" required><br>
        <input type="email" name="emailAdd" placeholder="邮箱地址" v-model="mailbox" required><br>
        <input type="text" name="confirm_code" placeholder="验证码" v-model="confirmcode" style="width:50%;" @keyup.enter="signUp()" required>
        <span><button style="width:25%; margin-left:12px; padding:5px;" @click="verify">获取</button></span><br><br>
        <span style="color:blue;font-size:20px;font-weight:800;cursor:pointer;" @click="changeView('forSignUp','forSignIn')">直接登录</span>
        <span><button style="width:40%; margin-left:12px;" @click="signUp">注册</button></span>
      </div>
      <div id="forReset" class="div_content">
        <div style="text-align:center;font-size:28px; line-height:20%;">
          <p>重置密码</p>
          <p style="font-family:monospace;font-style:italic;">Reset PWD</p>
        </div>
        <input type="text" name="user_name" placeholder="用户名" v-model="userID" required><br>
        <input type="password" name="pwd" placeholder="新密码" v-model="userPwd" required><br>
        <input type="password" name="ensurePwd" placeholder="确认密码" v-model="rePWD" required><br>
        <input type="email" name="emailAdd" placeholder="邮箱地址" v-model="mailbox" required><br>
        <input type="text" name="confirm_code" placeholder="验证码" v-model="confirmcode" style="width:50%;" required>
        <span><button style="width:25%; margin-left:12px; padding:5px;" @click="verify">获取</button></span><br><br>
        <span style="color:blue;font-size:20px;font-weight:800;cursor:pointer;" @click="changeView('forReset','forSignIn')">直接登录</span>
        <span><button style="width:40%; margin-left:12px;" @click="resetPwd" @keyup.enter="resetPwd">重置密码</button></span>
      </div>
     <!--*****************************************弹窗显示提示信息************************************-->
      <div id="msgShow">
      </div>
    </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import Slider from './Slider.vue'
export default {
  name: 'home',
  data: function () {
    return {
      remember: false,
      autoS: false,
      userID: '',
      userPwd: '',
      rePWD: '',
      mailbox: '',
      confirmcode: ''
    }
  },
  components: {//引入图片轮滑组件
    "v-slider": Slider
  },
  watch: {//监控各个变量的变化
    userID: function (val) {
      this.userID = val
    },
    userPwd: function (val) {
      this.userPwd = val
    },
    rePWD: function (val) {
      this.rePWD = val
    },
    mailbox: function (val) {
      this.mailbox = val
    },
    confirmcode: function (val) {
      this.confirmcode = val
    }
  },
  mounted () {//加载页面时检查是否登录
    this.init()
  },
  methods: {
    init: function () {//检查用户是否登录
      if (this.global.ifLogIn) {
        document.getElementById('login').style.display = 'none'
        document.getElementById('signup').style.display = 'none'
        document.getElementById('logout').style.display = 'block'
      } else {
        document.getElementById('login').style.display = 'block'
        document.getElementById('signup').style.display = 'block'
        document.getElementById('logout').style.display = 'none'
      }
    },
    toPage: function (page) {//页面跳转
      if (this.global.ifLogIn) {
        this.$router.push(page)
      } else {
        this.$options.methods.showmsg('请先登录！')
      }
    },
    showDiv: function (showdiv) {//显示弹窗，用于登录/注册/找回密码
      document.getElementById(showdiv).style.display = 'block'
      document.getElementById('bg_div').style.display = 'block'
      var bgDiv = document.getElementById('bg_div')
      bgDiv.style.width = document.body.scrollWidth
    },
    hideDiv: function () {//隐藏弹窗，显示主页面
      document.getElementById('forSignIn').style.display = 'none'
      document.getElementById('forSignUp').style.display = 'none'
      document.getElementById('forReset').style.display = 'none'
      document.getElementById('bg_div').style.display = 'none'
    },
    changeView: function (oldDiv, newDiv) {//用于注册/登录/找回密码间的跳转
      document.getElementById(oldDiv).style.display = 'none'
      document.getElementById(newDiv).style.display = 'block'
    },
    signIn: function () {//实现登录功能
      console.log(this.userID)
      console.log(this.rePWD)
      let formData = {
        'username': this.userID,
        'password': this.rePWD
      }
      var self = this
      axios({
        url: 'http://47.107.123.141/api/login',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        console.log(res.data)
        self.$options.methods.showmsg(res.data.message)
        if (res.data.code === 'success') {
          self.$options.methods.hideDiv()
          self.global.ifLogIn = true
          document.getElementById('login').style.display = 'none'
          document.getElementById('signup').style.display = 'none'
          document.getElementById('logout').style.display = 'block'
        }
      }).catch(function (err) {
        console.log(err)
        self.$options.methods.showmsg(err)
      })
    },
    resetPwd: function () {//实现找回（重置）密码功能
      console.log(this.userID)
      console.log(this.userPwd)
      console.log(this.rePWD)
      console.log(this.mailbox)
      console.log(this.confirmcode)
      let formData = {
        'username': this.userID,
        'password': this.userPwd,
        'password2': this.rePWD,
        'email': this.mailbox,
        'confirmcode': this.confirmcode
      }
      var self = this
      axios({
        url: 'http://47.107.123.141/api/reset',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        console.log(res.data)
        self.$options.methods.showmsg(res.data.message)
      }).catch(function (err) {
        console.log(err)
        self.$options.methods.showmsg(err)
      })
    },
    verify: function () {//获取验证码进行验证
      let formData = {
        'email': this.mailbox
      }
      var self = this
      axios({
        url: 'http://47.107.123.141/api/verify',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        console.log(res.data.code)
        self.$options.methods.showmsg(res.data.message)
      }).catch(function (err) {
        console.log(err)
        self.$options.methods.showmsg(err)
      })
    },
    signUp: function () {//实现注册功能
      console.log(this.userID)
      console.log(this.userPwd)
      console.log(this.rePWD)
      console.log(this.mailbox)
      console.log(this.confirmcode)
      let formData = {
        'username': this.userID,
        'password': this.userPwd,
        'password2': this.rePWD,
        'email': this.mailbox,
        'confirmcode': this.confirmcode
      }
      var self = this
      axios({
        url: 'http://47.107.123.141/api/register',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(formData)
      }).then(function (res) {
        console.log(res.data)
        self.$options.methods.showmsg(res.data.message)
      }).catch(function (err) {
        console.log(err)
        self.$options.methods.showmsg(err)
      })
    },
    logOut: function () {//实现登出功能
      this.global.ifLogIn = false
      this.$options.methods.showmsg('当前用户已退出')
      document.getElementById('login').style.display = 'block'
      document.getElementById('signup').style.display = 'block'
      document.getElementById('logout').style.display = 'none'
      /* axios({
        url: 'http://47.107.123.141/api/logout',
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: null
      }).then(function (res) {
        console.log(res.data)
        self.$options.methods.showmsg(res.data.message)
        if(res.data.code == 'success'){
          document.getElementById('login').style.display = 'block'
          document.getElementById('signup').style.display = 'block'
          document.getElementById('logout').style.display = 'none'
        }
      }).catch(function (err) {
        console.log(err)
        self.$options.methods.showmsg(err)
      }) */
    },
    showmsg: function (msg) {//用于显示各个操作需要给出的提示和信息
      document.getElementById('msgShow').innerHTML = msg
      document.getElementById('msgShow').style.display = 'block'
      setTimeout(function () { document.getElementById('msgShow').style.display = 'none' }, 5000)
    }
  }
}
</script>

<style>
<!--首页导航栏-->
  #header{
    top:0;
    position:sticky;
    background-color:white;
    z-index:900;
  }
  #logo{
    display: block;
    margin:auto;
    width:40%;
  }
  #menu{
    width:100%;
    display: inline-block;
    background-color: cornflowerblue;
    box-shadow:0 1px 1px #ccc;
    border-radius: 2px;
  }
  #menu a{
    display:block;
    padding:18px 30px;
    float:left;
    color:#fff;
    cursor:pointer;
    font-weight: bold;
    font-size:20px;
    text-decoration: none !important;
    line-height: 1;
  }
  #menu a:hover{
    background-color:rgb(56, 120, 238);
  }
  .bg_shadow{
    display: none;
    position:absolute;
    top:0;left:0;
    width:100%;height:100%;
    background-color: rgba(255, 255, 255, 0.95);
    z-index:1001;
  }
  .div_content{
    display: none;
    position:absolute;
    margin:auto;
    border:3px solid rgb(80, 80, 248);
    border-radius: 20px;
    top:50%;left:50%;
    -ms-transform: translate(-50%,-50%);
    transform: translate(-50%,-50%);
    z-index:1002;
  }
  #forSignIn{
    padding: 10px 40px 20px;
  }
  #forSignUp, #forReset{
    padding: 15px;
  }
  input[type=text], input[type=password],input[type=email],select{
    padding:12px 20px;
    margin:16px 0 0px;
    display: inline-block;
    border:1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  .div_content button{
    padding:5px 10px;
    margin:8px 0;
    width:100%;
    border:1px ridge cornflowerblue;
    border-radius: 4px;
    background:cornflowerblue;
    box-sizing: border-box;
  }
<!--首页内容-->
  div.picShow{
    margin:8px;
    border:1px solid #ccc;
    float:left;
    width:600px;
    height:400px;
  }
  div.picShow img{
    width:600px;
    height:auto;
  }
  #homeContent{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    margin-bottom: 50px;
    /*
    line-height:0.8;
    -webkit-column-count: 2;
    -moz-column-count: 2;
    column-count: 2;
    padding:20px;
    margin:10px;
    */
  }
  div.intro{
    height: 400px;
    width: 700px;
    min-width: 700px;
    margin-left: 50px;
    border:1px solid #ccc;
    font-size: 16px;
    /*
    margin:8px;
    border:1px solid #ccc;
    float:left;
    width:600px;
    height:400px;
    line-height:1.5;
    font-size:16px;
    */
  }
  #msgShow{
    display:none;
    border:2px solid lightblue;
    border-radius:10px;
    background:white;
    width:200px;
    height:auto;
    position:absolute;
    top:0;right:0;
    padding:10px;
    margin:20px;
    font-size:20px;
    font-weight:bold;
    overflow:hidden;
    transition:0.5s;
    z-index:10000;
    box-shadow:0px 8px 16px 0px rgba(100,149,237,0.6);
  }
</style>
