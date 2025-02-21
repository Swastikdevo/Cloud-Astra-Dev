```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  if (loading) return <div>Loading...</div>;

  const handleDelete = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <ul>
      {customers.map(customer => (
        <li key={customer.id}>
          {customer.name} - {customer.email} 
          <button onClick={() => handleDelete(customer.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

export default CustomerList;
```