// eslint.config.js
import vuetifyConfig from 'eslint-config-vuetify' // Import the default export from vuetify's config
import pluginPrettierRecommended from 'eslint-plugin-prettier/recommended'

export default [
  // Apply the Vuetify configuration(s)
  // If vuetifyConfig is an array (common for flat configs), spread it.
  // If it's a single config object, just include it.
  // Most shared configs export an array, so spreading is safer.
  ...(Array.isArray(vuetifyConfig) ? vuetifyConfig : [vuetifyConfig]),

  // Add Prettier configuration LAST.
  // pluginPrettierRecommended includes eslint-config-prettier (to turn off conflicting rules)
  // and sets up prettier as an ESLint rule.
  pluginPrettierRecommended,

  // Optional: You can add further customizations or your own rules here
  // For example, to customize Prettier's behavior reported by ESLint:
  /*
  {
    rules: {
      'prettier/prettier': ['warn', {
        // Your Prettier options (these should ideally match your .prettierrc file)
        // e.g., "singleQuote": true, "semi": false
      }],
      // Your other project-specific rules that are not for formatting
      // 'no-console': 'warn',
    }
  }
  */
]
