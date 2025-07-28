import { Linter } from 'eslint';

export default [
  {
    files: ['**/*.{js,ts,astro}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    plugins: {},
    rules: {
      semi: ['error', 'always'],
      quotes: ['error', 'single'],
    },
  },
];
