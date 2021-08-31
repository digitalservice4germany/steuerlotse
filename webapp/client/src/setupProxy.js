// This file is automatically loaded when starting the development server.

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    createProxyMiddleware(
      [
        '/**',                                     // Proxy all requests, except:
        '!**/*.js',                                // javascript,
        '!**/*.js.map',                            // source maps,
        '!**/*.css',                               // css,
        '!/{static,files,fonts,icons,images}/**',  // any other static assets,
        '!/*.hot-update.json',                     // HMR requests
      ],
      {
        target: 'http://localhost:5000',
        changeOrigin: true,
        autoRewrite: true,
      }
    )
  );
};

