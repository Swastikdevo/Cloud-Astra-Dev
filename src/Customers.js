```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newCustomer, setNewCustomer] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        setCustomers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const addCustomer = () => {
    const newCust = { name: newCustomer };
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCust),
    })
      .then(response => response.json())
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer('');
      });
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add new customer" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```