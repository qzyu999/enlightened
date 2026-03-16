// src/useTicTacToe.js
import { useState } from 'react';

export function useTicTacToe() {
  const [history, setHistory] = useState([{ squares: Array(9).fill(null) }]);
  const [stepNumber, setStepNumber] = useState(0);
  const xIsNext = stepNumber % 2 === 0;

  const current = history[stepNumber];
  const winner = calculateWinner(current.squares);
  const isDraw = !winner && current.squares.every(Boolean);

  function handleClick(i) {
    const historyUpToCurrent = history.slice(0, stepNumber + 1);
    const currentSquares = historyUpToCurrent[historyUpToCurrent.length - 1].squares;
    
    if (currentSquares[i] || winner) return;

    const nextSquares = currentSquares.slice();
    nextSquares[i] = xIsNext ? 'X' : 'O';
    
    setHistory(historyUpToCurrent.concat([{ squares: nextSquares }]));
    setStepNumber(historyUpToCurrent.length);
  }

  function jumpTo(step) {
    setStepNumber(step);
  }

  return {
    squares: current.squares,
    xIsNext,
    winner,
    isDraw,
    history,
    stepNumber,
    handleClick,
    jumpTo
  };
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];
  for (let [a, b, c] of lines) {
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}