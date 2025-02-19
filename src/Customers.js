```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [fetching, setFetching] = useState(true);
  
  useEffect(() => {
    const fetchCustomers = async () => {
      setFetching(true);
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setFetching(false);
    };
    fetchCustomers();
  }, []);

  const handleDelete = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (fetching) return <div>Loading...</div>;

  return (
    <div>
      <h1>Customer Management</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```