```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/customers')
      .then((response) => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then((data) => {
        setCustomers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  const handleDelete = (id) => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => {
        setCustomers(customers.filter((customer) => customer.id !== id));
      })
      .catch((err) => setError(err.message));
  };

  const handleEdit = (id) => {
    // Simple logic to change the state for customer editing
    const updatedCustomers = customers.map((customer) =>
      customer.id === id ? { ...customer, editing: true } : customer
    );
    setCustomers(updatedCustomers);
  };

  return (
    <div>
      <h1>Customer List</h1>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name}
            <button onClick={() => handleEdit(customer.id)}>Edit</button>
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```