module.exports = {
  "btsh-schema": {
    input: "http://localhost:8000/api/schema",
    output: {
      client: "fetch",
      baseUrl: "http://localhost:8000",
      prettier: true,
      target: "./src/schema.ts",
    },
  },
};
