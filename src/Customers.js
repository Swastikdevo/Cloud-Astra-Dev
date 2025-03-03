```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data))
      .catch(error => console.error('Error fetching customers:', error));
  }, []);

  const addCustomer = () => {
    const newCustomer = { name, email };
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    })
      .then(response => response.json())
      .then(data => setCustomers([...customers, data]))
      .catch(error => console.error('Error adding customer:', error));
    setName('');
    setEmail('');
  };

  const deleteCustomer = (id) => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => setCustomers(customers.filter(customer => customer.id !== id)))
      .catch(error => console.error('Error deleting customer:', error));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```