```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
    setLoading(false);
  };

  const addCustomer = async () => {
    if (newCustomer) {
      const response = await fetch('/api/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newCustomer }),
      });
      const data = await response.json();
      setCustomers([...customers, data]);
      setNewCustomer('');
    }
  };

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        value={newCustomer}
        onChange={(e) => setNewCustomer(e.target.value)}
        placeholder="Add new customer"
      />
      <button onClick={addCustomer}>Add</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```