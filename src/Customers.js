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

  const removeCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return loading ? (
    <div>Loading...</div>
  ) : (
    <ul>
      {customers.map(customer => (
        <li key={customer.id}>
          {customer.name} <button onClick={() => removeCustomer(customer.id)}>Remove</button>
        </li>
      ))}
    </ul>
  );
};

export default CustomerList;
```