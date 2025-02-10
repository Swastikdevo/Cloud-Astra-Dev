```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axios.get('/api/customers');
        setCustomers(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const handleDelete = async (id) => {
    await axios.delete(`/api/customers/${id}`);
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} 
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```