const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  //��������Invalid Host header����
  devServer: {
   historyApiFallback: true,
    allowedHosts: "all"
    // allowedHosts: [
    //   '49zh771913.yicp.fun', // ������ʵ�������ַ����������������͸�ĵ�ַ
    //   '.yicp.fun'   // .�Ƕ���������ͨ���
    // ],
  },
  transpileDependencies: true,
  lintOnSave:false
})

