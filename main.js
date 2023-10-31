const express = require("express");
const pool = require("./utils/dbConfig");
const fs = require("fs");
const bodyParser = require("body-parser");
const cors = require("cors");
const app = express();
const authRoutes = require("./v1_routes/auth");
const setsRoutes = require("./v1_routes/sets");
const foldersRoutes = require("./v1_routes/folders");
const flashcardsRoutes = require("./v1_routes/flashcards");
const statisticsRoutes = require("./v1_routes/statistics");
const utilsRoutes = require("./v1_routes/utils");
const helmet = require("helmet");

const port = process.env.PORT || 5500;
app.use(helmet());
app.use(
  bodyParser.urlencoded({
    limit: "5mb",
    parameterLimit: 100000,
    extended: false,
  })
);

// app.use(
//   cors({
//     origin: "https://mesembria-client-e8e2f2c0ffab.herokuapp.com",
//     optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
//   })
// );

app.use(cors());

app.use(
  bodyParser.json({
    limit: process.env.BODY_LIMIT || "5mb",
  })
);
app.settings("*", cors());
app.use(express.json());

app.use("/v1", authRoutes);
app.use("/v1", setsRoutes);
app.use("/v1", foldersRoutes);
app.use("/v1", flashcardsRoutes);
app.use("/v1", statisticsRoutes);
app.use("/v1", utilsRoutes);

app.listen(process.env.PORT || 5000, () => {
  console.log(
    `Server listening on the port::${process.env.PORT}`,
    process.env.DATABASE_URL
  );
});
