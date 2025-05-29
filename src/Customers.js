```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const addCustomer = async () => {
    const newCustomer = { name, email };
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const data = await response.json();
    setCustomers([...customers, data]);
    resetForm();
  };

  const updateCustomer = async () => {
    const updatedCustomer = { name, email };
    await fetch(`/api/customers/${editingId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedCustomer),
    });
    setCustomers(customers.map(c => (c.id === editingId ? { ...c, ...updatedCustomer } : c)));
    resetForm();
  };

  const editCustomer = (customer) => {
    setName(customer.name);
    setEmail(customer.email);
    setEditingId(customer.id);
  };

  const resetForm = () => {
    setName('');
    setEmail('');
    setEditingId(null);
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <form onSubmit={(e) => { e.preventDefault(); editingId ? updateCustomer() : addCustomer(); }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <button type="submit">{editingId ? 'Update' : 'Add'}</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => editCustomer(customer)}>Edit</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManager;
```