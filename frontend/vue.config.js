// import ParallelUglifyPlugin from './node_modules/webpack-parallel-uglify-plugin';
const ParallelUglifyPlugin = require('./node_modules/webpack-parallel-uglify-plugin');

module.exports = {
    chainWebpack: config => {
        config.module.rules.delete('eslint');
    },
    configureWebpack: {
        plugins: [
            // 使用 ParallelUglifyPlugin 并行压缩输出的 JS 代码
            new ParallelUglifyPlugin({
                // 传递给 UglifyJS 的参数
                uglifyJS: {
                    output: {
                        // 最紧凑的输出
                        beautify: false,
                        // 删除所有的注释
                        comments: false,
                    },
                    compress: {
                        // 在UglifyJs删除没有用到的代码时不输出警告
                        warnings: false,
                        // 删除所有的 `console` 语句，可以兼容ie浏览器
                        drop_console: true,
                        // 内嵌定义了但是只用到一次的变量
                        collapse_vars: true,
                        // 提取出出现多次但是没有定义成变量去引用的静态值
                        reduce_vars: true,
                    }
                },
            }),
        ],
    },
    pages: {
        home: {
            entry: 'src/spas/home/main.js',
            template: 'public/index.html',
            filename: 'home.html',
            title: 'Home Page',
            chunks: ['chunk-vendors', 'chunk-common', 'home']
        },
        user: {
            entry: 'src/spas/user/main.js',
            template: 'public/index.html',
            filename: 'user.html',
            title: 'User Page',
            chunks: ['chunk-vendors', 'chunk-common', 'user']
        },
        admin: {
          entry: 'src/spas/admin/main.js',
          template: 'public/index.html',
          filename: 'admin.html',
          title: 'Admin Page',
          chunks: ['chunk-vendors', 'chunk-common', 'admin']
        },
    },
    assetsDir: 'vstatic',
    configureWebpack: {
        devtool: 'source-map',
    },
    devServer: {
        index: 'home.html',
        historyApiFallback: {
            rewrites: [
                { from: /^\/user/, to: '/user.html'},
                { from: /^\/admin/, to: '/admin.html'},
                { from: /^\/home/, to: '/home.html'},
            ]
        },
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5050/api/',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
    outputDir: '../sspymgr/vuetemplates'
}