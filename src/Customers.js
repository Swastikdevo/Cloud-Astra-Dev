```javascript
import React, { useState, useEffect } from 'react';
import { fetchCustomers, deleteCustomer } from './api';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadCustomers = async () => {
      const data = await fetchCustomers();
      setCustomers(data);
      setLoading(false);
    };
    loadCustomers();
  }, []);

  const handleDelete = async (id) => {
    await deleteCustomer(id);
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Customer List</h1>
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

export default CustomerList;
```