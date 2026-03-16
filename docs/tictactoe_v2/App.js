// src/App.js
import React from 'react';
import { useTicTacToe } from './useTicTacToe';

const STYLES = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    color: '#1e293b',
    padding: '20px',
  },
  gameWrapper: {
    display: 'flex',
    flexDirection: 'row',
    gap: '40px',
    alignItems: 'flex-start',
    flexWrap: 'wrap',
    justifyContent: 'center'
  },
  header: { fontSize: '2.5rem', marginBottom: '1rem', color: '#334155' },
  status: {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '1.5rem',
    padding: '8px 16px',
    borderRadius: '8px',
    backgroundColor: '#ffffff',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  board: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 100px)',
    gridTemplateRows: 'repeat(3, 100px)',
    gap: '12px',
    padding: '12px',
    backgroundColor: '#cbd5e1',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  },
  square: (value) => ({
    width: '100px',
    height: '100px',
    backgroundColor: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '2rem',
    fontWeight: 'bold',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.2s ease',
    color: value === 'X' ? '#2563eb' : '#dc2626',
    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
  }),
  historyList: {
    listStyleType: 'none',
    padding: 0,
    maxHeight: '400px',
    overflowY: 'auto',
  },
  historyBtn: (isCurrent) => ({
    display: 'block',
    width: '100%',
    margin: '5px 0',
    padding: '8px 12px',
    fontSize: '0.9rem',
    backgroundColor: isCurrent ? '#334155' : '#ffffff',
    color: isCurrent ? 'white' : '#334155',
    border: '1px solid #cbd5e1',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: isCurrent ? 'bold' : 'normal',
  })
};

export default function TicTacToe() {
  const { 
    squares, winner, isDraw, xIsNext, history, stepNumber, handleClick, jumpTo 
  } = useTicTacToe();

  const status = winner 
    ? `Winner: ${winner}` 
    : isDraw 
      ? "It's a Draw!" 
      : `Next Player: ${xIsNext ? 'X' : 'O'}`;

  return (
    <div style={STYLES.container}>
      <h1 style={STYLES.header}>Tic Tac Toe</h1>
      <div style={STYLES.status}>{status}</div>
      
      <div style={STYLES.gameWrapper}>
        <div style={STYLES.board}>
          {squares.map((square, i) => (
            <button
              key={i}
              onClick={() => handleClick(i)}
              style={STYLES.square(square)}
            >
              {square}
            </button>
          ))}
        </div>

        <div>
          <h3>Move History</h3>
          <ul style={STYLES.historyList}>
            {history.map((_, move) => (
              <li key={move}>
                <button 
                  style={STYLES.historyBtn(move === stepNumber)} 
                  onClick={() => jumpTo(move)}
                >
                  {move ? `Go to move #${move}` : 'Go to game start'}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}