import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get('http://localhost:5000/books');
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  return (
    <div className="App">
      <h1>Book List</h1>
      <ul>
        {books.map(book => (
          <li key={book._id.$oid}>
            <h2>{book.nombre}</h2>
            <p>Año de publicación: {book.year}</p>
            <p>ISBN: {book.ISBN}</p>
            <p>Pages: {book.pages}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
