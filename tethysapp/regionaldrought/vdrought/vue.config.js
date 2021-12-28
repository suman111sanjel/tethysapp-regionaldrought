const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

module.exports = {
    outputDir: path.resolve(__dirname, '../public/build'),
    chainWebpack: (config) => {
        if (process.env.NODE_ENV === 'production') {
            // If you wish to remove the standard entry point
            config.entryPoints.delete('app')

            // then add your own
            config.entry('current')
                .add('./src/current.js')
                .end()
                .entry('outlook')
                .add('./src/outlook.js')
                .end()


            // config.module.loader('fonts').tap(options => {
            //     options.name = `static/regionaldrought/fonts/[name].[hash:8].[ext]`
            // })

            config.module.rule('fonts').use('url-loader')
                .loader('file-loader') // replaces the url-loader
                .tap(options => Object.assign(options, {
                    name: 'static/regionaldrought/fonts/[name].[ext]'
                }))

            config.module.rule('images').use('url-loader')
                .loader('file-loader') // replaces the url-loader
                .tap(options => Object.assign(options, {
                    name: 'static/regionaldrought/images/[name].[ext]'
                }))
            config.module.rule('svg').use('file-loader')
                .tap(options => Object.assign(options, {
                    name: 'static/regionaldrought/images/[name].[ext]'
                }))
            // config.plugin('html').tap((opts) => {
            //     opts[0].filename = '../../templates/regionaldrought/helloWorld.html';
            //     return opts;
            // });
        }
    },
    css: {
        extract: {
            filename: 'static/regionaldrought/css/[name].[contenthash].css',
            chunkFilename: 'static/regionaldrought/css/chunkName.[name].[contenthash].css',
        },
    },
    configureWebpack: {

        output: {
            filename: 'static/regionaldrought/js/[name].[hash].js',
            chunkFilename: 'static/regionaldrought/js/[name].[hash].js',
        },
        plugins: [
            new CleanWebpackPlugin(),
            // new HtmlWebpackPlugin({
            //     filename: process.env.NODE_ENV === "production" ? '../../templates/regionaldrought/Created_current.html' : 'Created_current.html',
            //     title: 'Hello world current',
            //     description: 'Hello world nepal',
            //     chunks: ['current', 'chunk-vendors', 'chunk-common'],
            //     template: './src/page-template.hbs'
            // }),
            // new HtmlWebpackPlugin({
            //     title: 'Hello world outlook',
            //     description: 'outlook',
            //     filename: process.env.NODE_ENV === "production" ? '../../templates/regionaldrought/Created_outlook.html' : 'Created_outlook.html',
            //     chunks: ['outlook', 'chunk-vendors', 'chunk-common'],
            //     template: './src/page-template.hbs'
            // })
        ],
        // optimization: {
        //     splitChunks: process.env.NODE_ENV === "development" ? false : true //or just process.env.NODE_ENV === "production"
        // }
    },

    pages: {
        'apps/regionaldrought/current': {
            entry: 'src/current.js',
            template: 'public/index.html',
            filename: process.env.NODE_ENV === "production" ? '../../templates/regionaldrought/Created_current.html' : 'apps/regionaldrought/current.html',
            title: 'Regional Drought - Current',
            chunks: ['chunk-vendors', 'chunk-common', 'apps/regionaldrought/current']
        },
        'apps/regionaldrought/outlook': {
            entry: 'src/outlook.js',
            template: 'public/index.html',
            filename: process.env.NODE_ENV === "production" ? '../../templates/regionaldrought/Created_outlook.html' : 'apps/regionaldrought/outlook.html',
            title: 'Regional Drought - Outlook',
            chunks: ['chunk-vendors', 'chunk-common', 'apps/regionaldrought/outlook']
        },
    }
};