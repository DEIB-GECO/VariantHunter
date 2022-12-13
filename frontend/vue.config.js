
module.exports = {
  transpileDependencies: ["vuetify"],
  assetsDir: "static", // For simple configuration of static files in Flask (the "static_folder='...../dist/static'" part in app.py)
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000/", // So that the client dev server can access your Flask routes under /api
      }
    },
  },
  publicPath: "/variant_hunter/",
};
