const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  // css: {
  //   modules: false
  // }
  // transpileDependencies: true,

  // assetsDir: '/public'

    devServer: {
      allowedHosts: [
        'newsmanager.com', 
        'localhost',
        '127.0.0.1'    
      ],
      port:8000,
    },
  
})
