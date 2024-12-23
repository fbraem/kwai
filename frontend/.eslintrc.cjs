module.exports = {
  root: true,
  // This tells ESLint to load the config from the package `eslint-config-kwai`
  extends: ['kwai'],
  settings: {
    next: {
      rootDir: [
        'apps/*/',
        'packages/*/',
      ],
    },
  },
};
