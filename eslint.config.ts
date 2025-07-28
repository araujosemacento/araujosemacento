import { defineConfig } from 'eslint/config';
import js from '@eslint/js';
import astro from 'eslint-plugin-astro';
import astroParser from 'astro-eslint-parser';
import svelte from 'eslint-plugin-svelte';
import tsParser from '@typescript-eslint/parser';
import tsEslint from '@typescript-eslint/eslint-plugin';
import type { ESLint } from 'eslint';

export default defineConfig([
  {
    ignores: ['.astro/**', '**/*.d.ts', 'node_modules/**', 'dist/**', 'eslint.config.ts'],
  },
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: {
      '@typescript-eslint': tsEslint as unknown as ESLint.Plugin,
    },
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json',
        sourceType: 'module',
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
  // Spread the Astro recommended configs
  ...astro.configs.recommended,
  {
    files: ['**/*.astro'],
    languageOptions: {
      parser: astroParser,
      parserOptions: {
        parser: tsParser,
        extraFileExtensions: ['.astro'],
      },
    },
  },
  // Spread the Svelte recommended configs
  ...svelte.configs.recommended,
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parserOptions: {
        parser: tsParser,
      },
    },
  },
  {
    rules: {
      semi: ['error', 'always'],
      quotes: ['error', 'single'],
    },
  },
]);
