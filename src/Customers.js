```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setCustomers(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`/api/customers/${id}`, { method: 'DELETE' });
      if (response.ok) {
        setCustomers(customers.filter(customer => customer.id !== id));
      }
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {customers.map(customer => (
        <li key={customer.id}>
          {customer.name}
          <button onClick={() => handleDelete(customer.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

export default CustomerList;
```