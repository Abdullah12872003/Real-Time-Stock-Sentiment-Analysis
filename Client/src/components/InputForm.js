import React from 'react';
import './InputForm.css';

function InputForm({ stock, setStock, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={stock}
        onChange={(e) => setStock(e.target.value)}
        placeholder="Enter stock name"
      />
      <button type="submit">Analyze</button>
    </form>
  );
}
export default InputForm;
