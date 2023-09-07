

import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import Router from "./router";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={Router} />
);
