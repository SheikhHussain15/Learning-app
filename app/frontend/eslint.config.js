/** @type {import('eslint').Linter.Config} */
const config = {
  root: true,
  extends: ["next/core-web-vitals", "next/typescript"],
  rules: {
    "@next/next/no-img-element": "off",
    "react-hooks/exhaustive-deps": "warn",
  },
};

module.exports = config;
