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

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {customers.map(customer => (
        <li key={customer.id}>
          <span>{customer.name}</span>
          <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

export default CustomerList;
```