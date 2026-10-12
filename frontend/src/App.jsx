
import { useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8001/api/v1/claims/verify";

const EXAMPLE_CLAIMS = [
  "Regular physical activity provides health benefits.",
  "Vitamin C supplements can prevent or cure all illnesses.",
  "Exercise improves cardiovascular fitness and cures every disease.",
  "Drinking lemon water cures diabetes.",
];

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

      const verificationResult = {
        ...data,
        claim: data.claim || trimmedClaim,
        checkedAt: new Date().toISOString(),
      };

      setResult(verificationResult);

      setHistory((previousHistory) => [
        verificationResult,
        ...previousHistory.filter(
          (item) => item.claim !== verificationResult.claim
        ),
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
    setClaim(item.claim || "");
    setResult(item);
    setError("");
  };

  const clearHistory = () => {
    setHistory([]);
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
        return "✕";

      case "PARTIALLY_TRUE":
        return "◐";

      default:
        return "?";
    }
  };

  const getVerdictLabel = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return "TRUE";

      case "FALSE":
        return "FALSE";

      case "PARTIALLY_TRUE":
        return "PARTIALLY TRUE";

      default:
        return "UNVERIFIED";
    }
  };

  const getConfidenceLabel = (confidence) => {
    const value = Number(confidence || 0);

    if (value >= 0.8) {
      return "High confidence";
    }

    if (value >= 0.5) {
      return "Moderate confidence";
    }

    return "Low confidence";
  };

  const formatConfidence = (confidence) => {
    const value = Number(confidence || 0);

    return `${Math.round(value * 100)}%`;
  };

  const formatDate = (dateString) => {
    if (!dateString) {
      return "";
    }

    try {
      return new Date(dateString).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return "";
    }
  };

  const evidence = Array.isArray(result?.evidence)
    ? result.evidence
    : Array.isArray(result?.supporting_evidence)
      ? result.supporting_evidence
      : [];

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">✓</div>

            <div>
              <h1>HealthVerify AI</h1>
              <p>Evidence-based health claim verification</p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            <span>System online</span>
          </div>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="badge">AI-POWERED VERIFICATION</div>

          <h2>
            Verify health claims with
            <br />
            <span>evidence.</span>
          </h2>

          <p>
            Submit a health-related claim and our system will retrieve relevant
            evidence from trusted sources before generating an evidence-based
            verification result.
          </p>
        </section>

        <section className="verification-card">
          <form onSubmit={handleSubmit}>
            <label htmlFor="claim">
              Enter a health claim
            </label>

            <textarea
              id="claim"
              value={claim}
              onChange={(event) => setClaim(event.target.value)}
              placeholder="Example: Regular physical activity provides health benefits."
              disabled={loading}
            />

            <div className="input-footer">
              <span>{claim.length} characters</span>

              <button type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Verifying...
                  </>
                ) : (
                  <>
                    Verify claim
                    <span>→</span>
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="examples-section">
            <span className="examples-label">TRY AN EXAMPLE</span>

            <div className="examples-list">
              {EXAMPLE_CLAIMS.map((example) => (
                <button
                  key={example}
                  type="button"
                  className="example-button"
                  onClick={() => handleExampleClick(example)}
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </section>

        {error && (
          <div className="error-message">
            <strong>Verification failed</strong>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <section className="results">
            <div className="results-header">
              <div>
                <div className="section-label">VERIFICATION RESULT</div>
                <h3>Your claim analysis</h3>
              </div>

              <div className={getVerdictClass(result.verdict)}>
                <span className="verdict-icon">
                  {getVerdictIcon(result.verdict)}
                </span>

                <span>
                  {getVerdictLabel(result.verdict)}
                </span>
              </div>
            </div>

            <div className="claim-display">
              <span>CLAIM</span>
              <p>{result.claim || claim}</p>
            </div>

            <div className="result-grid">
              <div className="result-panel">
                <div className="panel-label">CONFIDENCE</div>

                <div className="confidence-value">
                  {formatConfidence(result.confidence)}
                </div>

                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: formatConfidence(result.confidence),
                    }}
                  ></div>
                </div>

                <p className="explanation">
                  {getConfidenceLabel(result.confidence)}
                </p>
              </div>

              <div className="result-panel">
                <div className="panel-label">EXPLANATION</div>

                <p className="explanation">
                  {result.explanation ||
                    "No explanation was provided by the verification system."}
                </p>
              </div>
            </div>

            <div className="evidence-section">
              <div className="evidence-heading">
                <div>
                  <div className="section-label">
                    SUPPORTING EVIDENCE
                  </div>

                  <h3>Retrieved sources</h3>
                </div>

                <span className="evidence-count">
                  {evidence.length}{" "}
                  {evidence.length === 1 ? "source" : "sources"}
                </span>
              </div>

              {evidence.length > 0 ? (
                <div className="evidence-list">
                  {evidence.map((item, index) => {
                    const metadata = item.metadata || {};

                    const title =
                      item.title ||
                      metadata.title ||
                      metadata.source_file ||
                      `Evidence ${index + 1}`;

                    const source =
                      item.source ||
                      metadata.source ||
                      metadata.source_organization ||
                      "Unknown source";

                    const rawContent =
                      item.snippet ||
                      item.content ||
                      item.text ||
                      metadata.content ||
                      "No evidence content available.";

                    const content = rawContent
                      .replace(/^Title:.*\r?\n?/gm, "")
                      .replace(/^Source:.*\r?\n?/gm, "")
                      .replace(/^Source URL:.*\r?\n?/gm, "")
                      .replace(/^Topic:.*\r?\n?/gm, "")
                      .replace(/^Source organization:.*\r?\n?/gm, "")
                      .trim();

                    const sourceUrl =
                      item.source_url ||
                      metadata.source_url ||
                      metadata.url ||
                      "";

                    const relevanceValue =
                      item.relevance_score ??
                      item.relevance ??
                      metadata.relevance_score ??
                      null;

                    const relevance =
                      relevanceValue !== null
                        ? `${Math.round(Number(relevanceValue) * 100)}%`
                        : null;

                    const evidenceNumber = String(index + 1).padStart(
                      2,
                      "0"
                    );

                    return (
                      <article
                        className="evidence-card"
                        key={`${title}-${index}`}
                      >
                        <div className="evidence-top">
                          <div>
                            <div className="evidence-number">
                              EVIDENCE {evidenceNumber}
                            </div>

                            <h4>{title}</h4>
                          </div>

                          {relevance && (
                            <div className="relevance">
                              {relevance} relevant
                            </div>
                          )}
                        </div>

                        <div className="source">
                          <strong>SOURCE</strong> {source}
                        </div>

                        <p>{content}</p>

                        {sourceUrl && (
                          <a
                            href={sourceUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            View official source ↗
                          </a>
                        )}
                      </article>
                    );
                  })}
                </div>
              ) : (
                <div className="no-evidence">
                  No supporting evidence was retrieved for this claim.
                </div>
              )}
            </div>
          </section>
        )}

        {history.length > 0 && (
          <section className="history-section">
            <div className="history-heading">
              <div>
                <div className="section-label">RECENT ACTIVITY</div>
                <h3>Recent verifications</h3>
              </div>

              <button
                type="button"
                className="clear-history"
                onClick={clearHistory}
              >
                Clear history
              </button>
            </div>

            <div className="history-list">
              {history.map((item, index) => {
                const verdict = item.verdict || "UNVERIFIED";

                return (
                  <button
                    type="button"
                    className="history-item"
                    key={`${item.claim}-${index}`}
                    onClick={() => handleHistoryClick(item)}
                  >
                    <span className="history-main">
                      <span className="history-claim">
                        {item.claim}
                      </span>

                      <span className="history-time">
                        {formatDate(item.checkedAt)}
                      </span>
                    </span>

                    <span
                      className={`history-verdict history-${verdict
                        .toLowerCase()
                        .replace("_", "-")}`}
                    >
                      {getVerdictLabel(verdict)}
                    </span>
                  </button>
                );
              })}
            </div>
          </section>
        )}

        <section className="info-section">
          <div>
            <div className="info-icon">✓</div>

            <div>
              <h3>Evidence-based verification</h3>

              <p>
                Results are generated by comparing your claim with retrieved
                evidence and an AI language model. HealthVerify AI is an
                informational tool and does not replace advice, diagnosis, or
                treatment from a qualified healthcare professional.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer>
        HealthVerify AI · AI-Powered Health Claim Verification System
      </footer>
    </div>
  );
}

export default App;
