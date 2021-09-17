const rewireStyledComponents = require("react-app-rewire-styled-components");

module.exports = function override(config, env) {
  config = rewireStyledComponents(config, env);

  // Remove content hashes from js files (let flask-static-digest handle those).
  config.output.filename = config.output.filename.replace(
    "[contenthash:8].",
    ""
  );
  config.output.chunkFilename = config.output.chunkFilename.replace(
    "[contenthash:8].",
    ""
  );

  // Remove unneeded plugins.
  const removeThesePlugins = [
    "ManifestPlugin",
    "HtmlWebpackPlugin",
    "InlineChunkHtmlPlugin",
    "InterpolateHtmlPlugin",
  ];
  config.plugins = config.plugins.filter(
    (plugin) => !removeThesePlugins.includes(plugin.constructor.name)
  );

  // Reconfigure specific plugins.
  for (let plugin of config.plugins) {
    // Remove content hashes from css files.
    if (plugin.constructor.name === "MiniCssExtractPlugin") {
      plugin.options.filename = plugin.options.filename.replace(
        "[contenthash:8].",
        ""
      );
      plugin.options.chunkFilename = plugin.options.chunkFilename.replace(
        "[contenthash:8].",
        ""
      );
    }
  }

  // Create a single entry bundle.
  config.optimization.splitChunks.chunks = "async";

  return config;
};
