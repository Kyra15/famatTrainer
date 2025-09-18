import { useState } from "react";

export default function SendDataDemo() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    const dataToSend = { message }; // Whatever you want to send

    const res = await fetch("http://localhost:3001/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    });

    const result = await res.json();
    setResponse(result);
  };

  return (
    <div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="type stuff"
      />
      <button onClick={handleSubmit}>Send to Flask</button>

      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
    </div>
  );
}
