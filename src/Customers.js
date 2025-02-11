```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        if (!response.ok) throw new Error('Error fetching customers');
        const data = await response.json();
        setCustomers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        setCustomers(customers.filter(customer => customer.id !== id));
      } catch (err) {
        setError('Failed to delete customer');
      }
    }
  };

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <ul>
          {customers.map(customer => (
            <li key={customer.id}>
              {customer.name} - {customer.email}
              <button onClick={() => handleDelete(customer.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerList;
```