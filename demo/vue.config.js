const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  //域名访问Invalid Host header问题
  devServer: {
   historyApiFallback: true,
    allowedHosts: "all"
    // allowedHosts: [
    //   '49zh771913.yicp.fun', // 允许访问的域名地址，即花生壳内网穿透的地址
    //   '.yicp.fun'   // .是二级域名的通配符
    // ],
  },
  transpileDependencies: true,
  lintOnSave:false
})

