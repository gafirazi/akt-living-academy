import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const instance = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

export default instance;
