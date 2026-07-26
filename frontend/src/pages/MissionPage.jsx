import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { getMission, submitCode } from '../services/api';

const LANG_MAP = {
  python: { label: 'Python', monaco: 'python', starterKey: 'starter_python' },
  cpp: { label: 'C++', monaco: 'cpp', starterKey: 'starter_cpp' },
  java: { label: 'Java', monaco: 'java', starterKey: 'starter_java' },
  javascript: { label: 'JavaScript', monaco: 'javascript', starterKey: 'starter_js' },
};

export default function MissionPage({ onMissionComplete }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [mission, setMission] = useState(null);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showHint, setShowHint] = useState(0);
  const editorRef = useRef(null);

  useEffect(() => {
    loadMission();
  }, [id]);

  useEffect(() => {
    if (mission) {
      const starterKey = LANG_MAP[language].starterKey;
      setCode(mission[starterKey] || '// Write your solution here\n');
    }
  }, [language, mission]);

  const loadMission = async () => {
    try {
      const data = await getMission(id);
      setMission(data);
      setCode(data.starter_python || '');
    } catch (err) {
      console.error('Failed to load mission:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setOutput(null);
    try {
      const result = await submitCode(mission.id, language, code);
      setOutput(result);
      if (result.status === 'passed' && onMissionComplete) {
        onMissionComplete(result);
      }
    } catch (err) {
      setOutput({ status: 'error', error_message: err.message, test_results: [] });
    } finally {
      setSubmitting(false);
    }
  };

  const handleEditorMount = (editor) => {
    editorRef.current = editor;
  };

  if (loading) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-cyan)' }}>LOADING MISSION BRIEFING...</h3>
      </div>
    );
  }

  if (!mission) {
    return (
      <div className="flex-center" style={{ height: 'calc(100vh - 64px)' }}>
        <h3 style={{ color: 'var(--neon-red)' }}>MISSION NOT FOUND</h3>
      </div>
    );
  }

  return (
    <div className="editor-container">
      {/* Left Panel — Problem Statement */}
      <div className="editor-problem-panel">
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => navigate(-1)}
          style={{ marginBottom: '1rem' }}
        >
          ← Back
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1.2rem', color: 'var(--neon-cyan)' }}>{mission.title}</h2>
          <span className={`badge badge-${mission.difficulty.toLowerCase()}`}>
            {mission.difficulty}
          </span>
        </div>

        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
          {mission.subtitle} · ⭐ {mission.reputation_reward} reputation
        </p>

        {/* Problem description rendered as markdown-like content */}
        <div className="markdown-content">
          {mission.description.split('\n').map((line, i) => {
            if (line.startsWith('## ')) return <h2 key={i}>{line.replace('## ', '')}</h2>;
            if (line.startsWith('### ')) return <h3 key={i}>{line.replace('### ', '')}</h3>;
            if (line.startsWith('```')) return null;
            if (line.startsWith('Input:') || line.startsWith('Output:'))
              return <p key={i} style={{ fontFamily: 'var(--font-mono)', color: 'var(--neon-green)' }}>{line}</p>;
            if (line.trim() === '') return <br key={i} />;
            return <p key={i}>{line}</p>;
          })}
        </div>

        {/* Sample Test Cases */}
        {mission.sample_tests?.length > 0 && (
          <div style={{ marginTop: '1.5rem' }}>
            <h3 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem', letterSpacing: '0.1em' }}>
              SAMPLE TEST CASES
            </h3>
            {mission.sample_tests.map((tc, i) => (
              <div key={i} style={{
                background: 'var(--bg-primary)', borderRadius: 'var(--radius-md)',
                padding: '0.75rem 1rem', marginBottom: '0.5rem',
                border: '1px solid var(--border-subtle)',
                fontFamily: 'var(--font-mono)', fontSize: '0.8rem',
              }}>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Input:</div>
                <pre style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', whiteSpace: 'pre-wrap' }}>{tc.input}</pre>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Expected:</div>
                <pre style={{ color: 'var(--neon-green)', whiteSpace: 'pre-wrap' }}>{tc.expected}</pre>
              </div>
            ))}
          </div>
        )}

        {/* Hints */}
        {(mission.hint_1 || mission.hint_2) && (
          <div style={{ marginTop: '1.5rem' }}>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => setShowHint((prev) => Math.min(prev + 1, 2))}
              disabled={showHint >= 2}
            >
              💡 {showHint === 0 ? 'Show Hint' : showHint === 1 ? 'Show Hint 2' : 'All Hints Shown'}
            </button>
            {showHint >= 1 && mission.hint_1 && (
              <div style={{
                marginTop: '0.75rem', padding: '0.75rem 1rem',
                background: 'rgba(255, 215, 0, 0.05)', border: '1px solid rgba(255, 215, 0, 0.2)',
                borderRadius: 'var(--radius-md)', color: 'var(--neon-yellow)', fontSize: '0.85rem',
              }}>
                💡 Hint 1: {mission.hint_1}
              </div>
            )}
            {showHint >= 2 && mission.hint_2 && (
              <div style={{
                marginTop: '0.5rem', padding: '0.75rem 1rem',
                background: 'rgba(255, 102, 0, 0.05)', border: '1px solid rgba(255, 102, 0, 0.2)',
                borderRadius: 'var(--radius-md)', color: 'var(--neon-orange)', fontSize: '0.85rem',
              }}>
                💡 Hint 2: {mission.hint_2}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Right Panel — Code Editor + Output */}
      <div className="editor-code-panel">
        {/* Toolbar */}
        <div className="editor-toolbar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <select
              className="editor-language-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              {Object.entries(LANG_MAP).map(([key, val]) => (
                <option key={key} value={key}>{val.label}</option>
              ))}
            </select>

            {mission.is_solved && (
              <span style={{
                fontFamily: 'var(--font-display)', fontSize: '0.7rem',
                color: 'var(--neon-green)', letterSpacing: '0.1em',
              }}>
                ✓ SOLVED
              </span>
            )}
          </div>

          <button
            className="btn btn-success"
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting ? '⏳ Executing...' : '▶ Run Heist'}
          </button>
        </div>

        {/* Monaco Editor */}
        <div className="editor-wrapper">
          <Editor
            height="100%"
            language={LANG_MAP[language].monaco}
            value={code}
            onChange={(val) => setCode(val || '')}
            onMount={handleEditorMount}
            theme="vs-dark"
            options={{
              fontSize: 14,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              minimap: { enabled: false },
              padding: { top: 16 },
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 4,
              wordWrap: 'on',
              lineNumbersMinChars: 3,
              renderLineHighlight: 'all',
              suggestOnTriggerCharacters: true,
              quickSuggestions: true,
            }}
          />
        </div>

        {/* Output Panel */}
        <div className="editor-output-panel">
          {!output && !submitting && (
            <div style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
              💻 Press "Run Heist" to execute your code against test cases...
            </div>
          )}

          {submitting && (
            <div style={{ color: 'var(--neon-yellow)', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
              ⏳ Executing code... Stand by, operative.
            </div>
          )}

          {output && (
            <div>
              {/* Status Banner */}
              <div style={{
                padding: '0.75rem 1rem', borderRadius: 'var(--radius-md)',
                marginBottom: '1rem',
                background: output.status === 'passed'
                  ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 0, 64, 0.1)',
                border: `1px solid ${output.status === 'passed' ? 'rgba(0, 255, 136, 0.3)' : 'rgba(255, 0, 64, 0.3)'}`,
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              }}>
                <span style={{
                  fontFamily: 'var(--font-display)', fontSize: '0.85rem', fontWeight: 700,
                  color: output.status === 'passed' ? 'var(--neon-green)' : 'var(--neon-red)',
                  letterSpacing: '0.1em',
                }}>
                  {output.status === 'passed' ? '✅ HEIST SUCCESSFUL' :
                   output.status === 'compile_error' ? '❌ COMPILATION FAILED' :
                   output.status === 'timeout' ? '⏱️ TIME LIMIT EXCEEDED' :
                   '❌ HEIST FAILED'}
                </span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  {output.tests_passed}/{output.tests_total} tests · {output.total_time_ms}ms
                </span>
              </div>

              {/* Reputation gain */}
              {output.reputation_gained > 0 && (
                <div style={{
                  padding: '0.5rem 1rem', marginBottom: '0.75rem',
                  background: 'rgba(255, 215, 0, 0.08)', borderRadius: 'var(--radius-sm)',
                  fontFamily: 'var(--font-display)', fontSize: '0.8rem', color: 'var(--neon-yellow)',
                }}>
                  ⭐ +{output.reputation_gained} Reputation earned!
                </div>
              )}

              {/* District unlock notification */}
              {output.district_unlocked && (
                <div style={{
                  padding: '0.75rem 1rem', marginBottom: '0.75rem',
                  background: 'rgba(204, 0, 255, 0.08)',
                  border: '1px solid rgba(204, 0, 255, 0.3)',
                  borderRadius: 'var(--radius-md)',
                  fontFamily: 'var(--font-display)', fontSize: '0.8rem', color: 'var(--neon-purple)',
                }}>
                  🔓 NEW DISTRICT UNLOCKED: {output.district_unlocked.name}!
                </div>
              )}

              {/* Error message */}
              {output.error_message && (
                <pre style={{
                  fontFamily: 'var(--font-mono)', fontSize: '0.8rem',
                  color: 'var(--neon-red)', marginBottom: '0.75rem',
                  whiteSpace: 'pre-wrap',
                }}>
                  {output.error_message}
                </pre>
              )}

              {/* Test Results */}
              {output.test_results?.map((tr, i) => (
                <div key={i} className={`test-result ${tr.passed ? 'passed' : 'failed'}`}>
                  <span className="test-result-icon">{tr.passed ? '✅' : '❌'}</span>
                  <span>Test #{i + 1}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>
                    {tr.execution_time_ms}ms
                  </span>
                  {!tr.passed && tr.error && (
                    <span style={{ color: 'var(--neon-red)', fontSize: '0.75rem' }}>
                      — {tr.error}
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
