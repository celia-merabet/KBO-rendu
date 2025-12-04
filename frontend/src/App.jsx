import { useState } from "react";
import axios from "axios";

export default function App() {
  const [id, setId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const search = async () => {
    setError("");
    setResult(null);

    try {
      const r = await axios.get(`http://127.0.0.1:8000/enterprise/${id}`);
      setResult(r.data);
    } catch (e) {
      setError("Entreprise non trouvée");
    }
  };

  return (
    <div className="container">
      <h2>Recherche KBO</h2>

      <input
        type="text"
        placeholder="Numéro d'entreprise"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />

      <button onClick={search}>Rechercher</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <h3>Résultat :</h3>
          <p>Numéro : {result.enterprise_number}</p>
          <p>Dénomination : {result.denomination}</p>
          <p>Adresse : {result.address}</p>
          <p>Statut : {result.status}</p>
        </div>
      )}
    </div>
  );
}
