import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

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
    <div className="container">
      <h1 className="my-4">Books</h1>
      <div className="row">
        {books.map(book => (
          <div key={book._id.$oid} className="col-md-4 mb-4">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{book.nombre}</h5>
                <p className="card-text">Año de publicación: {book.year}</p>
                <p className="card-text">ISBN: {book.ISBN}</p>
                <p className="card-text">Páginas: {book.pages}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
