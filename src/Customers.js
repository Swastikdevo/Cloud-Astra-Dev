```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      });
  }, []);

  const deleteCustomer = id => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => {
        setCustomers(customers.filter(customer => customer.id !== id));
      });
  };

  const addCustomer = customer => {
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customer),
    })
      .then(response => response.json())
      .then(newCustomer => {
        setCustomers([...customers, newCustomer]);
      });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Customer List</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} 
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <button onClick={() => addCustomer({ name: 'New Customer' })}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```