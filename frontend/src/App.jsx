import { useState } from "react";
import axios from "axios";

function App() {

  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const [token, setToken] = useState("");

  const [question, setQuestion] = useState("");

  const [response, setResponse] = useState("");

  const [loading, setLoading] = useState(false);


  // =========================
  // Login
  // =========================

  const login = async () => {

    try {

      const formData = new FormData();

      formData.append("username", username);

      formData.append("password", password);

      const res = await axios.post(
        "http://127.0.0.1:8000/login",
        formData
      );

      setToken(res.data.access_token);

      alert(
        "Login Successful"
      );

    } catch (error) {

      alert(
        "Login Failed"
      );
    }
  };


  // =========================
  // Ask Question
  // =========================

  const askQuestion = async () => {

    if (!question) return;

    setLoading(true);

    try {

      const formData = new FormData();

      formData.append(
        "question",
        question
      );

      const res = await axios.post(

        "http://127.0.0.1:8000/chat",

        formData,

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      setResponse(
        res.data.response
      );

    } catch (error) {

      setResponse(
        "Error connecting to backend."
      );
    }

    setLoading(false);
  };


  return (

    <div
      style={{
        padding: "40px",
        fontFamily: "Arial"
      }}
    >

      <h1>
        Enterprise RAG Chatbot
      </h1>


      {/* ========================= */}
      {/* Login */}
      {/* ========================= */}

      <div style={{ marginTop: "20px" }}>

        <h2>
          Login
        </h2>

        <input

          type="text"

          placeholder="Username"

          value={username}

          onChange={(e) =>
            setUsername(e.target.value)
          }

          style={{
            padding: "10px",
            width: "300px",
            marginBottom: "10px"
          }}
        />

        <br />

        <input

          type="password"

          placeholder="Password"

          value={password}

          onChange={(e) =>
            setPassword(e.target.value)
          }

          style={{
            padding: "10px",
            width: "300px"
          }}
        />

        <br />

        <button

          onClick={login}

          style={{
            marginTop: "10px",
            padding: "10px 20px"
          }}
        >

          Login

        </button>

      </div>


      {/* ========================= */}
      {/* Chat */}
      {/* ========================= */}

      <div style={{ marginTop: "40px" }}>

        <textarea

          rows="5"

          placeholder="Ask question..."

          value={question}

          onChange={(e) =>
            setQuestion(e.target.value)
          }

          style={{
            width: "500px",
            padding: "10px"
          }}
        />

        <br />

        <button

          onClick={askQuestion}

          style={{
            marginTop: "20px",
            padding: "10px 20px"
          }}
        >

          Ask

        </button>

      </div>


      {/* ========================= */}
      {/* Response */}
      {/* ========================= */}

      <div style={{ marginTop: "40px" }}>

        <h2>
          Response
        </h2>

        {

          loading

          ?

          <p>Loading...</p>

          :

          <div
            style={{
              width: "700px",
              whiteSpace: "pre-wrap",
              backgroundColor: "#f4f4f4",
              padding: "20px",
              borderRadius: "10px"
            }}
          >

            {response}

          </div>
        }

      </div>

    </div>
  );
}

export default App;