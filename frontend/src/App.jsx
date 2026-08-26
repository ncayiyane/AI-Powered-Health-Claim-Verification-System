import { useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000/api/v1/claims/verify";

function App() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyClaim = async () => {
    const trimmedClaim = claim.trim();

    if (!trimmedClaim) {
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
          claim: trimmedClaim,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      setResult(data);

      setHistory((previousHistory) => [
        {
          ...data,
          checkedAt: new Date().toISOString(),
        },
        ...previousHistory,
      ].slice(0, 5));
    } catch (err) {
      console.error("Verification error:", err);

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

  const handleExampleClick = (example) => {
    setClaim(example);
    setError("");
    setResult(null);
  };

  const handleHistoryClick = (item) => {
    setClaim(item.claim);
    setResult(item);
    setError("");
  };

  const getVerdictClass = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return "verdict-card verdict-true";

      case "FALSE":
        return "verdict-card verdict-false";

      case "PARTIALLY_TRUE":
        return "verdict-card verdict-partial";

      default:
        return "verdict-card verdict-unverified";
    }
  };

  const getVerdictIcon = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return "✓";

      case "FALSE":
        return "×";

      case "PARTIALLY_TRUE":
        return "◐";

      default:
        return "?";
    }
  };

  const formatVerdict = (verdict) => {
    if (verdict === "PARTIALLY_TRUE") {
      return "Partially True";
    }

    if (verdict === "TRUE") {
      return "True";
    }

    if (verdict === "FALSE") {
      return "False";
    }

    return "Unverified";
  };

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 0.8) {
      return "High confidence";
    }

    if (confidence >= 0.5) {
      return "Moderate confidence";
    }

    return "Low confidence";
  };

  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.8) {
      return "confidence-high";
    }

    if (confidence >= 0.5) {
      return "confidence-moderate";
    }

    return "confidence-low";
  };

  const getHistoryVerdictClass = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return "history-verdict history-true";

      case "FALSE":
        return "history-verdict history-false";

      case "PARTIALLY_TRUE":
        return "history-verdict history-partially-true";

      default:
        return "history-verdict history-unverified";
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon" aria-hidden="true">
              +
            </div>

            <div>
              <h1>HealthVerify AI</h1>
              <p>AI-Powered Health Claim Verification</p>
            </div>
          </div>

          <div className="system-status">
            <span className="status-dot"></span>
            <span>System Online</span>
          </div>
        </div>
      </header>

      <main className="main">
        {/* Hero */}
        <section className="hero">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            AI HEALTH VERIFICATION
          </div>

          <h2>
            Verify health claims with{" "}
            <span>trusted evidence.</span>
          </h2>

          <p>
            Enter a health-related claim and our AI system will compare it
            against retrieved evidence to determine whether it is true,
            false, partially true, or currently unverified.
          </p>
        </section>

        {/* Verification Form */}
        <section className="verification-card">
          <div className="card-header">
            <div>
              <span className="card-eyebrow">CLAIM CHECKER</span>
              <h3>What would you like to verify?</h3>
            </div>

            <div className="ai-badge">
              <span>AI</span>
              Evidence-based
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <label htmlFor="claim">Health claim</label>

            <textarea
              id="claim"
              value={claim}
              onChange={(event) => {
                setClaim(event.target.value);

                if (error) {
                  setError("");
                }
              }}
              placeholder="Example: Drinking lemon water cures diabetes."
              maxLength={1000}
              disabled={loading}
              aria-describedby="claim-counter"
            />

            <div className="input-footer">
              <span id="claim-counter">
                {claim.length}/1000 characters
              </span>

              <button
                type="submit"
                disabled={loading || !claim.trim()}
                className="verify-button"
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing claim...
                  </>
                ) : (
                  <>
                    Verify Claim
                    <span className="button-arrow" aria-hidden="true">
                      →
                    </span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Example Claims */}
          <div className="examples">
            <span>Try an example:</span>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleExampleClick(
                  "Regular physical activity provides health benefits."
                )
              }
              disabled={loading}
            >
              Physical activity
            </button>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleExampleClick(
                  "Vitamin C supplements can prevent or cure all illnesses."
                )
              }
              disabled={loading}
            >
              Vitamin C
            </button>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleExampleClick(
                  "Drinking lemon water cures diabetes."
                )
              }
              disabled={loading}
            >
              Lemon water
            </button>
          </div>

          {/* Error */}
          {error && (
            <div className="error-message" role="alert">
              <div className="error-icon">!</div>

              <div>
                <strong>Verification failed</strong>
                <p>{error}</p>
              </div>
            </div>
          )}
        </section>

        {/* Results */}
        {result && (
          <section className="results" aria-live="polite">
            <div className="results-header">
              <div>
                <span className="section-label">VERIFICATION RESULT</span>
                <h3>Your claim analysis</h3>
              </div>

              <div className={getVerdictClass(result.verdict)}>
                <div className="verdict-icon">
                  {getVerdictIcon(result.verdict)}
                </div>

                <div>
                  <span className="verdict-label">VERDICT</span>
                  <strong>{formatVerdict(result.verdict)}</strong>
                </div>
              </div>
            </div>

            {/* Claim */}
            <div className="claim-display">
              <div className="claim-label">
                <span>CLAIM</span>
              </div>

              <p>"{result.claim}"</p>
            </div>

            {/* Analysis */}
            <div className="result-grid">
              <div className="result-panel confidence-panel">
                <div className="panel-heading">
                  <span className="panel-label">CONFIDENCE</span>

                  <span
                    className={`confidence-status ${getConfidenceClass(
                      result.confidence
                    )}`}
                  >
                    {getConfidenceLabel(result.confidence)}
                  </span>
                </div>

                <div className="confidence-value">
                  {Math.round(result.confidence * 100)}
                  <span>%</span>
                </div>

                <div
                  className="confidence-bar"
                  aria-label={`Confidence ${Math.round(
                    result.confidence * 100
                  )}%`}
                >
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${Math.round(result.confidence * 100)}%`,
                    }}
                  ></div>
                </div>
              </div>

              <div className="result-panel explanation-panel">
                <span className="panel-label">EXPLANATION</span>

                <p className="explanation">
                  {result.explanation}
                </p>
              </div>
            </div>

            {/* Evidence */}
            <div className="evidence-section">
              <div className="evidence-heading">
                <div>
                  <span className="section-label">
                    SUPPORTING EVIDENCE
                  </span>

                  <h3>Retrieved sources</h3>
                </div>

                <div className="evidence-count">
                  <span>{result.evidence.length}</span>
                  {result.evidence.length === 1 ? " source" : " sources"}
                </div>
              </div>

              {result.evidence.length === 0 ? (
                <div className="no-evidence">
                  <div className="no-evidence-icon">?</div>

                  <div>
                    <strong>No supporting evidence found</strong>

                    <p>
                      The system could not retrieve relevant supporting
                      sources for this claim.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="evidence-list">
                  {result.evidence.map((item, index) => (
                    <article
                      className="evidence-card"
                      key={`${item.title}-${index}`}
                    >
                      <div className="evidence-top">
                        <div className="evidence-title-group">
                          <div className="evidence-number">
                            EVIDENCE {String(index + 1).padStart(2, "0")}
                          </div>

                          <h4>{item.title}</h4>
                        </div>

                        <div className="relevance">
                          <span>
                            {Math.round(item.relevance_score * 100)}%
                          </span>
                          relevant
                        </div>
                      </div>

                      <div className="source">
                        <span className="source-icon">✓</span>

                        <div>
                          <span className="source-label">SOURCE</span>
                          <strong>{item.source}</strong>
                        </div>
                      </div>

                      <div className="evidence-snippet">
                        {item.snippet}
                      </div>

                      {item.url && (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-link"
                        >
                          View official source
                          <span aria-hidden="true">↗</span>
                        </a>
                      )}
                    </article>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Recent Verification History */}
        {history.length > 0 && (
          <section className="history-section">
            <div className="history-heading">
              <div>
                <span className="section-label">RECENT ACTIVITY</span>

                <h3>Recent verifications</h3>
              </div>

              <button
                type="button"
                className="clear-history"
                onClick={() => setHistory([])}
              >
                Clear history
              </button>
            </div>

            <div className="history-list">
              {history.map((item, index) => (
                <button
                  type="button"
                  className="history-item"
                  key={`${item.claim}-${index}`}
                  onClick={() => handleHistoryClick(item)}
                >
                  <div className="history-main">
                    <span className="history-claim">
                      {item.claim}
                    </span>

                    <span className="history-time">
                      {new Date(item.checkedAt).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>

                  <div className={getHistoryVerdictClass(item.verdict)}>
                    {formatVerdict(item.verdict)}
                  </div>
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Disclaimer */}
        <section className="info-section">
          <div className="info-icon" aria-hidden="true">
            ✓
          </div>

          <div>
            <h3>Evidence-based verification</h3>

            <p>
              Results are generated by comparing your claim with retrieved
              evidence and an AI language model. HealthVerify AI is an
              informational tool and does not replace advice, diagnosis,
              or treatment from a qualified healthcare professional.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer>
        <p>
          HealthVerify AI
          <span>•</span>
          AI-Powered Health Claim Verification System
        </p>
      </footer>
    </div>
  );
}

export default App;