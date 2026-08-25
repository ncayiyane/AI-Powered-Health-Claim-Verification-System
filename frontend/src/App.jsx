import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/v1/claims/verify";

function App() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyClaim = async () => {
    if (!claim.trim()) {
      setError("Please enter a health claim to verify.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          claim: claim.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to verify the claim. Please make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    verifyClaim();
  };

  const getVerdictClass = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return "verdict true";

      case "FALSE":
        return "verdict false";

      case "PARTIALLY_TRUE":
        return "verdict partial";

      default:
        return "verdict unverified";
    }
  };

  const formatVerdict = (verdict) => {
    if (verdict === "PARTIALLY_TRUE") {
      return "PARTIALLY TRUE";
    }

    return verdict;
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">✚</div>

            <div>
              <h1>HealthVerify AI</h1>
              <p>AI-Powered Health Claim Verification</p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            System Online
          </div>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <span className="badge">AI HEALTH VERIFICATION</span>

          <h2>
            Verify health claims with
            <span> trusted evidence.</span>
          </h2>

          <p>
            Enter a health-related claim and our AI system will analyze
            trusted sources to determine whether the claim is true,
            false, partially true, or currently unverified.
          </p>
        </section>

        <section className="verification-card">
          <form onSubmit={handleSubmit}>
            <label htmlFor="claim">Health claim</label>

            <textarea
              id="claim"
              value={claim}
              onChange={(event) => setClaim(event.target.value)}
              placeholder="Example: Drinking lemon water cures diabetes."
              maxLength={1000}
              disabled={loading}
            />

            <div className="input-footer">
              <span>{claim.length}/1000</span>

              <button type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    Verify Claim
                    <span>→</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              <strong>Verification failed</strong>
              <p>{error}</p>
            </div>
          )}
        </section>

        {result && (
          <section className="results">
            <div className="results-header">
              <div>
                <span className="section-label">VERIFICATION RESULT</span>
                <h3>Your claim analysis</h3>
              </div>

              <div className={getVerdictClass(result.verdict)}>
                {formatVerdict(result.verdict)}
              </div>
            </div>

            <div className="claim-display">
              <span>CLAIM</span>
              <p>"{result.claim}"</p>
            </div>

            <div className="result-grid">
              <div className="result-panel">
                <span className="panel-label">CONFIDENCE</span>

                <div className="confidence-value">
                  {Math.round(result.confidence * 100)}%
                </div>

                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${Math.round(result.confidence * 100)}%`,
                    }}
                  ></div>
                </div>
              </div>

              <div className="result-panel">
                <span className="panel-label">EXPLANATION</span>

                <p className="explanation">
                  {result.explanation}
                </p>
              </div>
            </div>

            <div className="evidence-section">
              <div className="evidence-heading">
                <div>
                  <span className="section-label">SUPPORTING EVIDENCE</span>
                  <h3>Retrieved sources</h3>
                </div>

                <span className="evidence-count">
                  {result.evidence.length} source
                  {result.evidence.length !== 1 ? "s" : ""}
                </span>
              </div>

              {result.evidence.length === 0 ? (
                <div className="no-evidence">
                  No supporting evidence was retrieved.
                </div>
              ) : (
                <div className="evidence-list">
                  {result.evidence.map((item, index) => (
                    <article className="evidence-card" key={index}>
                      <div className="evidence-top">
                        <div>
                          <span className="evidence-number">
                            EVIDENCE {index + 1}
                          </span>

                          <h4>{item.title}</h4>
                        </div>

                        <span className="relevance">
                          {Math.round(item.relevance_score * 100)}% relevant
                        </span>
                      </div>

                      <div className="source">
                        <strong>Source:</strong> {item.source}
                      </div>

                      <p>{item.snippet}</p>

                      {item.url && (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View source →
                        </a>
                      )}
                    </article>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        <section className="info-section">
          <div>
            <span className="info-icon">✓</span>

            <div>
              <h3>Evidence-based verification</h3>

              <p>
                Results are generated using retrieved evidence and an
                AI language model. The system does not replace advice
                from qualified healthcare professionals.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <p>
          HealthVerify AI · AI-Powered Health Claim Verification System
        </p>
      </footer>
    </div>
  );
}

export default App;