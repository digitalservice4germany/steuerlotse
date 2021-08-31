module.exports = {
    "env": {
        "browser": true,
        "es2021": true,
        "jest/globals": true
    },
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:jest/recommended",
    "prettier"
    "parserOptions": {
        "ecmaFeatures": {
            "jsx": true
        },
        "ecmaVersion": 12,
        "sourceType": "module"
    },
    "plugins": [
        "react",
        "jest"
    ],
    "rules": {
        "react/react-in-jsx-scope": "off"
    },
    "settings": {
        "react": {
            "version": "detect",
        }
    },
    "overrides": [
        {
          "files": [
            "src/setupProxy.js"
          ],
          "env": {
            "node": true
          }
        }
    ]
};
